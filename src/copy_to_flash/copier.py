from asyncio.log import logger
import logging
import os
from math import floor
from threading import Lock
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

class SourceFile():
    def __init__(self, path, attr1="", attr2="") -> None:
        self.path = path
        self.attr1 = attr1
        self.attr2 = attr2

class Source(object):
    def paths_in_order() -> List[SourceFile]:
        raise NotImplementedError()

class ProgressTick(object):
    def __init__(self, process_file: SourceFile, file_index: int, total_files: int):
        self.file = process_file
        self.file_index = file_index
        self.total_files = total_files
    
    def percent(self) -> int:
        if self.total_files == 0:
            return 0
        return floor((self.file_index * 1.0 / self.total_files) * 100)

class ProcessHandler(object):
    def on_process(self, tick: ProgressTick):
        pass

    def on_finish(self, total: int):
        pass

    def on_canceled(self):
        pass

class CleanHandler(ProcessHandler):
    def on_before_clear(self, files: List[SourceFile]) -> bool:
        # do clear
        return True


class CopyHandler(ProcessHandler):
    def on_before_copy(self, files: List[SourceFile]) -> List[SourceFile]:
        # by default no handle
        return files


class CopyController(object):
    def __init__(self):
        self.__copier: CopyAlgo = None
        self.__clear_handler = CleanHandler()
        self.__copy_handler = CopyHandler()

        self.__mu = Lock()
        self.__canceled = False

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

    def cancel(self):
        self.__set_cancel(True)

    def __set_cancel(self, v: bool):
        self.__mu.acquire()
        self.__canceled = v
        self.__mu.release()

    def is_canceled(self):
        canceled = False

        self.__mu.acquire()
        canceled = self.__canceled
        self.__mu.release()

        return canceled
    
    def __process_list(self, l: List[SourceFile], action, preprocessor: ProcessHandler):
        i = 0
        for f in l:
            if self.is_canceled():
                try:
                    preprocessor.on_canceled()
                except BaseException as e:
                    logger.info('Process canceled error {}'.format(e))
                
                return

            tick = ProgressTick(process_file=f, file_index=i, total_files=len(l))
            preprocessor.on_process(tick)
            i = i + 1
            action(f)
    
    def __clear_folder(self, dir_path: str, recursive: bool) -> bool:
        logging.debug("path to clear {}".format(dir_path))
        files: List[SourceFile] = []
        dirs: List[SourceFile] = []

        for root_dir, ds, fs in os.walk(dir_path, topdown=False):
            logging.debug("aaaa {}".format(root_dir))
            if len(ds) > 0:
                if not recursive:
                    raise DirectoryHaveSubDirs(dir_path)
                else:
                    for adir in ds:
                        sub_dir = os.path.join(root_dir, adir)
                        logging.debug("path to clear - dir: {}".format(sub_dir))
                        dirs.append(SourceFile(sub_dir))
            for f in fs:
                f_path = os.path.join(root_dir, f)
                logging.debug("path to clear - file: {}".format(f_path))
                files.append(SourceFile(f_path))
            
        all_for_before: List[SourceFile] = [SourceFile(f.path) for f in files]
        all_for_before.extend([SourceFile(d.path) for d in dirs])

        logging.debug("for delete: {}".format(len(all_for_before)))
        
        if len(all_for_before) == 0:
            return True
        
        if not self.__clear_handler.on_before_clear(all_for_before):
            logging.debug("deciline remove")
            return False
        
        logging.debug("Start remove general files")

        self.__process_list(files, lambda f: os.remove(f.path), self.__clear_handler)
        
        logging.debug("Start remove dirs")

        self.__process_list(dirs, lambda d: os.rmdir(d.path), self.__clear_handler)

        self.__clear_handler.on_finish(len(all_for_before))
        
        return True

    def copy(self, source: Source, destination_dir: str):
        self.__set_cancel(False)

        if not source:
            raise NotSource()
        if not self.__copier:
            raise NotCopier()

        check_is_dir_exists(destination_dir)
        files = source.paths_in_order()
        logger.debug("files in the source {}".format(len(files)))
        if not files:
            raise NotFilesInSource()

        if not self.__clear_folder(destination_dir, True):
            return

        files = self.__copy_handler.on_before_copy(files)
        if files is None:
            return

        copy = lambda f: self.__copier.copy(f.path, destination_dir)
        
        self.__process_list(files, copy, self.__copy_handler)

        if not self.is_canceled():
            self.__copy_handler.on_finish(len(files))
 