import logging
from tkinter import StringVar, IntVar
from typing import List, Callable, Tuple

from copier import CopyController, SourceFile
from copiers.limit_size_dir_copier import LimitDirSizeCopier
from copiers.simple_copier import SimpleCopier
from source.dir import ListSource
from source.music_sorter import MusicDirSource
from gui.widgets.column_list import ListAdapter
from device import FlashDevice, AvailableDevices


class FileSourceListAdapter(ListAdapter):
    def __init__(self, list: List[SourceFile]) -> None:
        super().__init__(list)

    def vals(self, o: SourceFile) -> List[str]:
        return [o.attr1, o.attr2, o.path]

    def columns(self) -> List[str]:
        return ["Title", "Artist", "File"]


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
        self.source_dir = StringVar()
        self.dir_limit_size = IntVar()
        self._available_devices = AvailableDevices(device_getter)

    def get_available_devices(self) -> AvailableDevices:
        return self._available_devices

    def sorters(self) -> Tuple[List[str], StringVar]:
        return ([k for k, _ in self._sortiers.items()], self.sorter)
    
    def copiers(self) -> Tuple[List[str], StringVar]:
        return ([k for k, _ in self._copiers.items()], self.copier)

    def start_copy(self):
        dest_dir = self._available_devices.get_destination_dir()
        source_dir = self.source_dir.get()
        sorter_key = self.sorter.get()
        copier_key = self.copier.get()
        limit_dir_size = self.dir_limit_size.get()
        logging.debug("Start copy with params:\nDestination dir: {}\nSource dir: {}\nSorter: {}\nCopier: {}\nLimit dir size: {}".format(
            dest_dir,
            source_dir,
            sorter_key,
            copier_key,
            limit_dir_size
        ))

        sorter_constructor = self._sortiers.get(sorter_key)
        if not sorter_constructor:
            raise ValueError('Sorter "{}" is incorrect'.format(sorter_key))
        
        copier_costructor = self._copiers.get(copier_key)
        if not copier_costructor:
            raise ValueError('Copier "{}" is incorrect'.format(copier_key))

        copier = copier_costructor(limit_dir_size)
        sorter = sorter_constructor(source_dir)
        source = ListSource(sorter.paths_in_order())

        c = CopyController(source_dir)
        c.set_copier(copier)

        #c.copy(source=source, destination_dir="")
        raise NotImplementedError()

    