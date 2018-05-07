from Exceptions import NotFilesInSource
from math import floor


class MusicCopier(object):
    def __init__(self, source_dir, dest_dir, filter_obj, on_delete, on_progress):
        self.__source = source_dir
        self.__dest = dest_dir
        self.__filter = filter_obj
        self.__on_delete = on_delete
        self.__on_progress = on_progress

    def __call__(self):
        self.run()

    def run(self):
        files = self.__source.linear_files_list(self.__filter)
        if not files:
            raise NotFilesInSource()
        self.__dest.clear_folder(self.__on_delete)
        all_files = len(files)
        past_percent = 0
        i = 0
        self.__on_progress(past_percent, i, all_files)
        for path in files:
            self.__dest.copy_here(path)
            i += 1
            cur_percent = floor((i / all_files) * 100)
            if cur_percent > past_percent:
                self.__on_progress(cur_percent, i, all_files)
                past_percent = cur_percent
