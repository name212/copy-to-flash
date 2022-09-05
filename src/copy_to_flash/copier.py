from asyncio.log import logger
import logging
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

class NotSource(Exception):
    pass

class NotCopier(Exception):
    pass

class CancelClearDestination(Exception):
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
    def __init__(self):
        self.__copier: CopyAlgo = None
        self.__clear_handler = CleanHandler()
        self.__copy_handler = CopyHandler()

    def set_copier(self, copier: CopyAlgo):
        if not copier:
            return
        self.__copier = copier
    
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
            tick = ProgressTick(process_file=f, file_index=i, total_files=len(l))
            preprocessor.on_process(tick)
            i = i + 1
            action(f)
    
    def __clear_folder(self, dir_path: str, recursive: bool):
        logging.debug("path to clear {}".format(dir_path))
        files: List[str] = []
        dirs: List[str] = []

        for root_dir, ds, fs in os.walk(dir_path):
            logging.debug("aaaa {}".format(root_dir))
            if len(ds) > 0:
                if not recursive:
                    raise DirectoryHaveSubDirs(dir_path)
                else:
                    for adir in ds:
                        sub_dir = os.path.join(root_dir, adir)
                        logging.debug("path to clear - dir: {}".format(sub_dir))
                        dirs.append(sub_dir)
            for f in fs:
                f_path = os.path.join(root_dir, f)
                logging.debug("path to clear - file: {}".format(f_path))
                files.append(f_path)
            
        all_for_before = files.copy()
        all_for_before.extend(dirs)

        logging.debug("for delete: {}".format(len(all_for_before)))
        
        if len(all_for_before) == 0:
            return
        
        if not self.__clear_handler.on_before_clear(all_for_before):
            logging.debug("deciline remove")
            raise CancelClearDestination()
        
        logging.debug("Start remove general files")

        self.__process_list(files, os.remove, self.__clear_handler)
        
        logging.debug("Start remove dirs")

        self.__process_list(dirs, os.rmdir, self.__clear_handler)

        self.__clear_handler.on_finish(len(all_for_before))


    def copy(self, source: Source, destination_dir: str):
        if not source:
            raise NotSource()
        if not self.__copier:
            raise NotCopier()

        check_is_dir_exists(destination_dir)
        files = source.paths_in_order()
        logger.debug("files in the source {}".format(len(files)))
        if not files:
            raise NotFilesInSource()

        self.__clear_folder(destination_dir, True)

        copy = lambda f: self.__copier.copy(f, destination_dir)
        
        self.__process_list(files, copy, self.__copy_handler)

        self.__copy_handler.on_finish(len(files))
 