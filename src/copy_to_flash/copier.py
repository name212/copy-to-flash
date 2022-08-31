import os
from math import floor
from typing import List


def check_is_dir_exists(dir: str):
    if not os.path.exists(dir) or not os.path.isdir(dir):
        raise Exception("{} is not dir".format(dir))

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

class ProgressTick(object):
    def __init__(self, process_file: str, file_index: int, total_files: int):
        self.file = process_file
        self.file_index = file_index
        self.total_files = total_files
    
    def percent(self) -> int:
        return floor((self.file_index * 1.0 / self.total_files) * 100)

class ProcessHandler(object):
    def on_process(self, tick: ProgressTick):
        pass

    def on_finish(self, total: int):
        pass

class CleanHandler(ProcessHandler):
    def on_before_clear(self, files: List[str]) -> bool:
        # do clear
        return True


class CopyHandler(ProcessHandler):
    pass


class CopyController(object):
    def __init__(self, copier: CopyAlgo):
        self.__copier = copier
        self.__clear_handler = CleanHandler()
        self.__copy_handler = CopyHandler()
    
    def set_clear_handler(self, handler: CleanHandler):
        if not handler:
            return
        self.__clear_handler = handler

    def set_copy_handler(self, handler: CopyHandler):
        if not handler:
            return
        self.__copy_handler = handler
    
    def __process_list(self, l: List[str], action, preprocessor: ProcessHandler):
        i = 0
        for f in l:
            tick = ProgressTick(process_file=f, file_index=i, total=len(l))
            preprocessor.on_process(tick)
            i = i + 1
            action(f)
    
    def __clear_folder(self, dir_path: str, recursive: bool):
        files: List[str] = []
        dirs: List[str] = []

        for dir_name, dirs, files in os.walk(dir_path):
            if len(dirs) > 0:
                if not recursive:
                    raise DirectoryHaveSubDirs(dir_path)
                else:
                    for adir in dirs:
                        dirs.append(os.path.join(dir_name, adir))
            for file in files:
                files.append(os.path.join(dir_name, file))
            break

        all_for_before = files.copy().extend(dirs)
        
        if len(all_for_before) == 0:
            return

        if not self.__clear_handler.on_before_clear(all_for_before):
            return
        
        self.__process_list(files, os.remove, self.__clear_handler)

        self.__process_list(dirs, os.rmdir, self.__clear_handler)

        self.__clear_handler.on_finish()


    def copy(self, source: Source, destination_dir: str):
        check_is_dir_exists(destination_dir)
        files = source.paths_in_order()
        if not files:
            raise NotFilesInSource()
        self.__clear_folder(destination_dir, True)

        copy = lambda f: self.__copier.copy(f, destination_dir)
        
        self.__process_list(files, copy, self.__copy_handler)

        self.__copy_handler.on_finish()
 