class DirectoryHaveSubDirs(Exception):
    pass


class NotDir(Exception):
    pass


class Directory(object):
    def clear_folder(self, recursive, on_deleted):
        raise NotImplementedError()

    def linear_files_list(self, filter_path):
        raise NotImplementedError()
