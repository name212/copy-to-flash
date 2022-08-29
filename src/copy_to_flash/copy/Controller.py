from math import floor
from typing import List
import shutil
import os
from fs.dir import check_is_dir_exists


class NotFilesInSource(Exception):
    pass


class DirectoryHaveSubDirs(Exception):
    pass


class CopyAlgo(object):
    def copy(self, source_file_path: str, destination_dir_path: str):
        raise NotImplementedError()


class Source(object):
    def paths_in_order() -> List[str]:
        raise NotImplementedError()


def _empty(file):
    pass


class CopyController(object):
    def __init__(self, copier):
        self.__copier = copier
        self.__on_delete = _empty
        self.__on_progress = None
    
    def set_on_delete(self, on_delete):
        self.__on_delete = on_delete

    def set_on_delete(self, on_progress):
        self.__on_progress = on_progress
    
    def __clear_folder(self, dir_path: str, recursive: bool):
        for dir_name, dirs, files in os.walk(dir_path):
            if len(dirs) > 0:
                if not recursive:
                    raise DirectoryHaveSubDirs(dir_path)
                else:
                    for adir in dirs:
                        path = os.path.join(dir_name, adir)
                        shutil.rmtree(path)
                        self.__on_delete(path)
            for file in files:
                full_path = os.path.join(dir_name, file)
                os.remove(full_path)
                self.__on_delete(full_path)
            break
    

    def copy(self, source: Source, destination_dir: str):
        check_is_dir_exists(destination_dir)
        files = source.paths_in_order()
        if not files:
            raise NotFilesInSource()
        self.__clear_folder(destination_dir, True)
        all_files = len(files)
        past_percent = 0
        i = 0
        self.__on_progress(past_percent, i, all_files)
        for path in files:
            self.__copier.copy(path, destination_dir)
            i += 1
            cur_percent = floor((i / all_files) * 100)
            if cur_percent > past_percent:
                if self.__on_progress:
                    self.__on_progress(cur_percent, i, all_files)
                past_percent = cur_percent
 