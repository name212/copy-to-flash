import shutil

from copier import CopyAlgo

class SimpleCopier(CopyAlgo):
    def copy(self, source_file_path: str, destination_dir_path: str):
        shutil.copy(source_file_path, destination_dir_path)
