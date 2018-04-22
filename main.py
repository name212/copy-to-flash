import os
import platform

from ArgumentParser import parse as parse_argument
from Exceptions import UnsupportedPlatform
from console.ConsoleFactory import ConsoleFactory
from PartitionChoiser import get_destination_partition

_VERSION = "0.0.1"
_EXIT_CODES = {
    'NORMAL': 0
}


def get_available_getter():
    sys = platform.system()
    if sys == "Linux":
        from platforms.LinuxFlashDevice import get_available_devices
        return get_available_devices

    raise UnsupportedPlatform(sys)


def get_files_list(dir_path, filter_path):
    paths = []
    for dir_name, dirs, files in os.walk(dir_path, followlinks=True):
        for file in files:
            path = os.path.join(dir_name, file)
            info = filter_path(path)
            if info:
                paths.append(info)
    return paths


if __name__ == "__main__":
    factory = ConsoleFactory()
    controller = factory.get_controller()
    get_available_devices = get_available_getter()
    available_devices = get_available_devices()
    args = parse_argument(available_devices)
    if args.show_version:
        factory.get_view().show_version(_VERSION, lambda: exit(_EXIT_CODES['NORMAL']))

    dest = get_destination_partition(available_devices, args, lambda parts: controller.choice_dest_partition(parts))
    print(dest)
