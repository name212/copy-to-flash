import logging
import platform
import sys
from typing import List

from cli.run import ArgumentError, NotAvailableDestinationDevices, run as cli_run
from gui.app import App
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
    start_gui = False
    devices = available_devices()
    try:
        cli_run(devices, _VERSION)
    except (NotAvailableDestinationDevices, ArgumentError) as e:
        start_gui = True
        # todo gui here
    except BaseException as e:
        logging.error("Got error {}".format(e))
        sys.exit(1)    
    
    if start_gui:
        app = App()
        app.run(devices, _VERSION)


