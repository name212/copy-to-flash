import os
import shutil
from FileSystem import Directory, DirectoryHaveSubDirs


def _empty(file):
    pass


class PythonDirectory(Directory):
    def __init__(self, path):
        if not os.path.exists(path) or not os.path.isdir(path):
            raise Exception("{} is not dir".format(path))
        self.__path = path

    def linear_files_list(self, filter_path):
        for dir_name, dirs, files in os.walk(self.__path, followlinks=True):
            for file in files:
                path = os.path.join(dir_name, file)
                filter_path.process_path(path)

        return filter_path.get_sort_paths_list()

    def clear_folder(self, recursive, on_delete=_empty):
        for dir_name, dirs, files in os.walk(self.__path):
            if len(dirs) > 0:
                if not recursive:
                    raise DirectoryHaveSubDirs(self.__path)
                else:
                    for adir in dirs:
                        path = os.path.join(dir_name, adir)
                        shutil.rmtree(path)
                        on_delete(path)
            for file in files:
                full_path = os.path.join(dir_name, file)
                os.remove(full_path)
                on_delete(full_path)
            break

    def copy_here(self, path):
        shutil.copy(path, self.__path)
