import argparse


from Arguments import Arguments
from platforms.PythonDirectory import PythonDirectory
from PartitionChoiser import get_destination_partition


class DirParameter(object):
    def __call__(self, param):
        try:
            directory = PythonDirectory(param)
        except:
            raise ValueError('Argument "{}" is not dir'.format(param))

        return directory

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
    def __init__(self, available_devices, charact_produser, message='unknown'):
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


class ConsoleArguments(Arguments):
    def __init__(self, removable_devices, controller, version_str):
        arg_parser = argparse.ArgumentParser(description='Flash copy')
        arg_parser.add_argument('-s', '--source-dir', dest='source_dir', type=DirParameter())
        arg_parser.add_argument('-d', '--dest-device', dest='dest_device', type=RemovableDevicePath(removable_devices))
        arg_parser.add_argument('-p', '--dest-part', dest='dest_part', type=RemovablePartitionPath(removable_devices))
        arg_parser.add_argument('-m', '--dest-mount', dest='dest_part',
                                type=RemovablePartitionMountPoint(removable_devices))
        arg_parser.add_argument('--version', dest='show_version', action='version',
                                version='Version {}'.format(version_str))
        arg_parser.add_argument('-v', '--verbose', dest='verbose', action='store_const', const=True)
        self.__args = arg_parser.parse_args()
        self.__part = get_destination_partition(
            removable_devices,
            self.__args,
            lambda parts: controller.choice_dest_partition(parts)
        )

    def get_destination(self):
        return self.__part

    def is_verbose(self):
        return self.__args.verbose

    def get_source(self):
        return self.__args.source_dir
