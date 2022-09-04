import platform
from typing import List

from copier import CopyController
from device import FlashDevice
from cli.arguments import ConsoleArguments
from cli.handlers import ConsoleClearHandler, ConsoleCopyHandler

_VERSION = "0.1.0"

class UnsupportedPlatform(Exception):
    pass


def available_devices() -> List[FlashDevice]:
    sys = platform.system()
    if sys == "Linux":
        from platforms.linux import get_available_devices
        return get_available_devices()

    raise UnsupportedPlatform(sys)


if __name__ == "__main__":
    devices = available_devices()
    args = ConsoleArguments(
        removable_devices=devices,
        version_str=_VERSION
    )

    copier = CopyController(args.get_copier())

    copier.set_clear_handler(ConsoleClearHandler(args.is_verbose()))
    copier.set_copy_handler(ConsoleCopyHandler())

    copier.copy(args.get_source(), args.get_destination())
