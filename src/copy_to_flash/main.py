import platform
from typing import List

from cli.run import ArgumentError, run as cli_run
from device import FlashDevice

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
    try:
        cli_run(devices, _VERSION)
    except ArgumentError as e:
        # todo gui here
        raise e
    except:
        raise     

