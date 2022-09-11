from tkinter import StringVar
from typing import List, Callable

from copier import CopyAlgo, CopyController
from copiers.limit_size_dir_copier import LimitDirSizeCopier
from copy_to_flash.source.dir import ListSource
from copy_to_flash.source.music_sorter import MusicDirSource

from device import FlashDevice

class Controller(object):
    def __init__(self, device_getter: Callable[[], List[FlashDevice]]) -> None:
        self._device_getter = device_getter
        self._source_dir = StringVar()
    
    def start_copy(self):
        c = CopyController()
        source = MusicDirSource(self._source_dir.get())
        source = ListSource(source.paths_in_order())
        c.copy(source=source, destination_dir="")

    