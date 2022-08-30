from typing import List
import os

from ..copier import check_is_dir_exists
from src.copy_to_flash.copier import Source


class Sorter(object):
    def process_path(self, path: str):
        raise NotImplementedError()

    def sort(self) -> List[str]:
        raise NotImplementedError()


class DirSource(Source):
    def __init__(self, dir_path: str, sorter: Sorter):
        check_is_dir_exists(dir_path)
        self.__path = dir_path
        self.__sorter = sorter

    def paths_in_order(self) -> List[str]:
        for dir_name, dirs, files in os.walk(self.__path, followlinks=True):
            for file in files:
                path = os.path.join(dir_name, file)
                self.__sorter.process_path(path)

        return self.__sorter.sort()