import logging
import platform
import sys
from sys import stdout
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
    strfmt = '[%(asctime)s] [%(name)s] [%(levelname)s] > %(message)s'
    datefmt = '%Y-%m-%d %H:%M:%S'
    
    logging.basicConfig(stream=stdout, level=logging.DEBUG, format=strfmt, datefmt=datefmt)
    
    try:
        devices = available_devices()
        cli_run(devices, _VERSION)
    except (NotAvailableDestinationDevices, ArgumentError) as e:
        start_gui = True
    except BaseException as e:
        logging.error("Got error {}".format(e))
        sys.exit(1)    
    
    if start_gui:
        app = App(_VERSION)
        app.run(available_devices)


