import logging
from tkinter import StringVar, IntVar
from typing import List, Callable, Tuple

from copier import CopyAlgo, CopyController
from copiers.limit_size_dir_copier import LimitDirSizeCopier
from copiers.simple_copier import SimpleCopier
from source.dir import ListSource
from source.music_sorter import MusicDirSource

from device import FlashDevice

class Controller(object):
    def __init__(self, device_getter: Callable[[], List[FlashDevice]]) -> None:
        self._device_getter = device_getter

        self._sortiers = {
            "By title (Asc)": lambda p: MusicDirSource(p, False),
            "By title (Desc)": lambda p: MusicDirSource(p, True),
        }

        self._copiers = {
            "Simple": lambda _: SimpleCopier(),
            "Limit dir size": lambda p: LimitDirSizeCopier(p),
        }

        self._available_devices = [d.get_title() for d in device_getter()]
        logging.debug("available devices {}", self._available_devices)

        self.source_dir = StringVar()
        self.partition_dir = StringVar()
        self.sorter = StringVar()
        self.copier = StringVar()
        self.dir_limit_size = IntVar()

    def get_available_devices(self) -> Tuple[List[str], StringVar]:
        return (self._available_devices, self.partition_dir)

    def sorters(self) -> Tuple[List[str], StringVar]:
        return ([k for k, _ in self._sortiers.items()], self.sorter)
    
    def copiers(self) -> Tuple[List[str], StringVar]:
        return ([k for k, _ in self._copiers.items()], self.copier)

    def start_copy(self):
        c = CopyController()
        source = MusicDirSource(self.source_dir.get())
        source = ListSource(source.paths_in_order())
        c.copy(source=source, destination_dir="")

    