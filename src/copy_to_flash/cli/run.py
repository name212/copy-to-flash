import logging
from sys import stdout
from typing import List, Optional

from copier import CopyAlgo, CopyController
from copiers.limit_size_dir_copier import LimitDirSizeCopier
from .handlers import ConsoleClearHandler, ConsoleCopyHandler
from source.music_sorter import MusicDirSource
from .arguments import ConsoleArguments, Args
from device import FlashDevice, Partition
from .input import choice_dest_partition, get_partition_from_device


class NotAvailableDestinationDevices(Exception):
    pass

class ArgumentError(Exception):
    def __init__(self, msg: str) -> None:
        super().__init__(msg)
        self.clause = msg

def __get_destination_partition(removable_devices: List[FlashDevice], prog_args: Args) -> Optional[Partition]:
    # have destination partition. return it
    if prog_args.dest_part:
        return prog_args.dest_part
    # have removable device. show count partitions
    if prog_args.dest_device:
        return get_partition_from_device(prog_args.dest_device)
    
    # not partition or device: user choice from all partitions
    all_parts: List[Partition] = []
    for d in removable_devices:
        all_parts += d.get_partitions()
    return choice_dest_partition(all_parts)

def run(available_devices: List[FlashDevice], version: str):
    args = ConsoleArguments(
        removable_devices=available_devices,
        version_str=version
    ).get_args()


    logLvl = logging.WARN

    if args.verbose:
        logLvl= logging.DEBUG
    
    logging.basicConfig(stream=stdout, level=logLvl)

    logging.debug("arguments={}".format(args))

    if not args.source_dir or args.source_dir == "":
        raise ArgumentError("source is required")
    
    part = args.dest_part

    if not available_devices:
        raise NotAvailableDestinationDevices

    if not args.dest_part:
        part = __get_destination_partition(available_devices, args)
        if not part:
            raise ArgumentError("destination partition is required")
        logging.debug("choiced part device: {} | {}".format(
            part.get_label(),
            part.get_dev_file(),
        ))

    dest_dir = part.get_mount()
    
    logging.debug("destinatin dir: {}".format(dest_dir))

    copier: CopyAlgo = args.copier
    if not copier:
        copier = LimitDirSizeCopier(max_files_in_dir=512)
    
    logging.debug("copy algo {}".format(copier))

    source = MusicDirSource(args.source_dir)

    c = CopyController()
    c.set_copier(copier)
    c.set_clear_handler(ConsoleClearHandler(args.verbose))
    c.set_copy_handler(ConsoleCopyHandler())

    c.copy(source, dest_dir)