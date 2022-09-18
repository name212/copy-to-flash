from tkinter import StringVar, IntVar
from typing import List, Callable, Tuple

from copier import CopyController
from copiers.limit_size_dir_copier import LimitDirSizeCopier
from copiers.simple_copier import SimpleCopier
from source.dir import ListSource
from source.music_sorter import MusicDirSource

from device import FlashDevice, AvailableDevices


class Controller(object):
    def __init__(self, device_getter: Callable[[], List[FlashDevice]]) -> None:
        self._sortiers = {
            "By title (Asc)": lambda p: MusicDirSource(p, False),
            "By title (Desc)": lambda p: MusicDirSource(p, True),
        }

        self._copiers = {
            "Simple": lambda _: SimpleCopier(),
            "Limit dir size": lambda p: LimitDirSizeCopier(p),
        }

        self.sorter = StringVar()
        self.copier = StringVar()
        self.dir_limit_size = IntVar()
        self._available_devices = AvailableDevices(device_getter)

    def get_available_devices(self) -> AvailableDevices:
        return self._available_devices

    def sorters(self) -> Tuple[List[str], StringVar]:
        return ([k for k, _ in self._sortiers.items()], self.sorter)
    
    def copiers(self) -> Tuple[List[str], StringVar]:
        return ([k for k, _ in self._copiers.items()], self.copier)

    def start_copy(self):
        c = CopyController()
        source = MusicDirSource(self.source_dir.get())
        source = ListSource(source.paths_in_order())
        c.copy(source=source, destination_dir="")

    