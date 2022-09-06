import os
from typing import List

from copier import Source, SourceFile, check_is_dir_exists


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

    def paths_in_order(self) -> List[SourceFile]:
        for dir_name, dirs, files in os.walk(self.__path, followlinks=True):
            for file in files:
                path = os.path.join(dir_name, file)
                self.__sorter.process_path(path)

        return self.__sorter.sort()
