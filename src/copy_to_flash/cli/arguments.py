import argparse
from typing import List, Optional

from copier import CopyAlgo, Source, check_is_dir_exists
from copiers.limit_size_dir_copier import LimitDirSizeCopier
from copiers.simple_copier import SimpleCopier
from device import FlashDevice, Partition
from source.music_sorter import MusicDirSource
from .input import choice_dest_partition, get_partition_from_device


class DirParameter(object):
    def __call__(self, param):
        try:
             check_is_dir_exists(param)
        except:
            raise ValueError('Argument "{}" is not dir'.format(param))

        return param

    def __str__(self):
        return 'DirParameter'


class RemovableDevicePath(object):
    def __init__(self, available_devices):
        self.__devices = available_devices

    def __call__(self, param):
        for device in self.__devices:
            if device.get_dev_file() == param:
                return device
        raise ValueError('Argument "{}" is not removable device'.format(param))

    def __str__(self):
        return 'RemovableDevicePath'


class PartitionValidator(object):
    def __init__(self, available_devices: List[FlashDevice], charact_produser, message='unknown'):
        self.__devices = available_devices
        self.__func = charact_produser
        self.__message = message

    def __call__(self, param):
        for device in self.__devices:
            for part in device.get_partitions():
                if self.__func(part) == param:
                    return part
        raise ValueError('Argument "{}" is not {}'.format(param, self.__message))


class RemovablePartitionPath(PartitionValidator):
    def __init__(self, available_devices):
        super().__init__(
            available_devices,
            lambda p: p.get_dev_file(),
            'removable device partition')

    def __str__(self):
        return 'RemovablePartitionPath'


class RemovablePartitionMountPoint(PartitionValidator):
    def __init__(self, available_devices):
        super().__init__(available_devices, lambda p: p.get_mount(), 'removable device mount point')

    def __str__(self):
        return 'RemovablePartitionMountPoint'


class CopierParam(object):
    def __call__(self, param):
        if not param:
            return SimpleCopier()

        copier_name, copier_param_1 = param
        copier_obj = None
        if copier_name == 'simple':
            copier_obj = SimpleCopier()
        elif copier_name == 'limit_size':
            dir_size = 512
            if copier_param_1 is not None:
                dir_size = int(copier_param_1)
            copier_obj = LimitDirSizeCopier(dir_size)
        else:
            raise ValueError('Copier type "{}" not support. Use "simple" or "limit_size [size]"'.format(param))

        return copier_obj

    def __str__(self):
        return 'CopierType'

class Args(object):
    def __init__(self):
        self.source_dir: str = ""
        self.copier: CopyAlgo = None
        self.dest_part: Partition = None
        self.verbose: bool = False

def get_destination_partition(removable_devices: List[FlashDevice], prog_args: Args) -> Optional[Partition]:
    # have destination partition. return it
    if prog_args.dest_part:
        return prog_args.dest_part
    # have removable device. show count partitions
    if prog_args.dest_device:
        return get_partition_from_device(prog_args.dest_device)
    
    if not removable_devices:
        return None

    # not partition or device: user choice from all partitions
    all_parts: List[Partition] = []
    for d in removable_devices:
        all_parts += d.get_partitions()
    return choice_dest_partition(all_parts)


class ConsoleArguments(object):
    def __init__(self, removable_devices:  List[FlashDevice], version_str):
        arg_parser = argparse.ArgumentParser(description='Flash copy')
        arg_parser.add_argument('-s', '--source-dir', dest='source_dir', type=DirParameter())
        arg_parser.add_argument('-c', '--copier', dest='copier', nargs='+', type=CopierParam())
        arg_parser.add_argument('-d', '--dest-device', dest='dest_device', type=RemovableDevicePath(removable_devices))
        arg_parser.add_argument('-p', '--dest-part', dest='dest_part', type=RemovablePartitionPath(removable_devices))
        arg_parser.add_argument('-m', '--dest-mount', dest='dest_part',
                                type=RemovablePartitionMountPoint(removable_devices))
        arg_parser.add_argument('--version', dest='show_version', action='version',
                                version='Version {}'.format(version_str))
        arg_parser.add_argument('-v', '--verbose', dest='verbose', action='store_const', const=True)
        self.__args  = arg_parser.parse_args()

        self.args = Args()

        self.args.dest_part = get_destination_partition(
            removable_devices,
            self.__args
        )
        self.args.copier = self.__args.copier
        self.args.source_dir = self.__args.source_dir
        self.args.verbose = self.__args.verbose

    def get_args(self) -> Args:
        return self.args
