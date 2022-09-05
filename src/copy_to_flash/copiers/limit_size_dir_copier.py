import shutil
import os

from copier import CopyAlgo


class _NumberDirNameGenerator:
    def __init__(self, start_from=0, max_iters=100):
        self._cur = start_from
        if max_iters < 1:
            raise ValueError("Incorrect max_iters params. Must be positive")

        self._max_iters = max_iters
        self._cur_iter = 0

    def __call__(self, *args, **kwargs):
        self._cur_iter += 1

        if self._cur_iter > self._max_iters:
            raise StopIteration()

        res = str(self._cur)
        self._cur += 1
        return res

class LimitDirSizeCopier(CopyAlgo):
    def __init__(self, max_files_in_dir=512, sub_dir_name_gen=None):
        if max_files_in_dir < 1:
            raise ValueError("Incorrect max_files in_dir. Must be positive")
        self._max = max_files_in_dir
        self._name_gen = sub_dir_name_gen
        if not sub_dir_name_gen:
            self._name_gen = _NumberDirNameGenerator(0, max_files_in_dir)

        # чтобы при первом вызове copy создать поддиректорию
        self._cur_files_in_sub_dir = max_files_in_dir + 1

        self._cur_name = ''

    def copy(self, source_file_path, destination_dir_path):
        if self._cur_files_in_sub_dir > self._max:
            gen = self._name_gen
            self._cur_name = gen()
            self._cur_files_in_sub_dir = 0

        cur_dir_path = os.path.join(destination_dir_path, self._cur_name)
        # на всякий пожарный добавим / в конец
        cur_dir_path = os.path.join(cur_dir_path, '')
        if not os.path.exists(cur_dir_path):
            os.mkdir(cur_dir_path)
        if os.path.isfile(cur_dir_path):
            raise IOError("Not copy in {} because it's file, not dir".format(cur_dir_path))

        shutil.copy(source_file_path, cur_dir_path)
        self._cur_files_in_sub_dir += 1

    def __str__(self) -> str:
        return "LimitDirSizeCopier({})".format(self._max)
