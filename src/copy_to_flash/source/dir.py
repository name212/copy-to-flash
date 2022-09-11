import os
from typing import List

from copier import Source, SourceFile, check_is_dir_exists

class EmptyListException(Exception):
    pass

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

class ListSource(Source):
    def __init__(self, orig: List[SourceFile]):
        if not orig:
            raise EmptyListException()
        
        self.__list: List[SourceFile] = []
        self.__list.extend(orig)


    def paths_in_order(self) -> List[SourceFile]:
        return self.__list
    
    def swap(self, i: int, j: int):
        if i < 0 or i >= len(self.__list):
            raise ValueError("Incorrect first arg")
        
        if j < 0 or j >= len(self.__list):
            raise ValueError("Incorrect second arg")
        
        t = self.__list[i]
        self.__list[i] = self[j]
        self.__list[j] = t

    def delete(self, i: int):
        if i < 0 or i >= len(self.__list):
            raise ValueError("Incorrect index")
        del self.__list[i]