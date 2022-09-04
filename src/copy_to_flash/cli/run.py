from typing import List

from copier import CopyAlgo, CopyController
from copiers.limit_size_dir_copier import LimitDirSizeCopier
from .handlers import ConsoleClearHandler, ConsoleCopyHandler
from source.music_sorter import MusicDirSource
from .arguments import ConsoleArguments
from device import FlashDevice

class ArgumentError(Exception):
    def __init__(self, msg: str) -> None:
        super().__init__(msg)
        self.clause = msg

def run(available_devices: List[FlashDevice], version: str):
    args = ConsoleArguments(
        removable_devices=available_devices,
        version_str=version
    ).get_args()

    if not args.source_dir or args.source_dir:
        raise ArgumentError("source is required")
    
    if not args.dest_part:
        raise ArgumentError("destination partition is required")
    
    copier: CopyAlgo = args.copier
    if not copier:
        copier = LimitDirSizeCopier(max_files_in_dir=512)
    source = MusicDirSource(args.source_dir)

    c = CopyController()
    c.set_copier(copier)
    c.set_clear_handler(ConsoleClearHandler(args.verbose))
    c.set_copy_handler(ConsoleCopyHandler())

    copier.copy(source, args.dest_part)