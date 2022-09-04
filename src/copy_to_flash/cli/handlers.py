from typing import List

from copier import CleanHandler, CopyHandler, ProgressTick
from .input import read_yes_no


class ConsoleClearHandler(CleanHandler):
    def __init__(self, verbose: bool) -> None:
        super().__init__()
        self.verbose = verbose

    def on_before_clear(self, files: List[str]) -> bool:
        print("Do you want clear destination before copy?")
        if self.verbose:
            for f in files:
                print("\t{}".format(f))
        return read_yes_no()
    
    def on_process(self, tick: ProgressTick):
        if self.verbose:
            print("{} deleted".format(tick.file))

    def on_finish(self, total: int):
        if self.verbose:
            print("Destination device was cleaned. Removed {}".format(total))

class ConsoleCopyHandler(CopyHandler):
    def on_process(self, tick: ProgressTick):
        print("[{}/{} ({}%)] {}".format(tick.file_index, tick.total_files, tick.percent(), tick.file))
    
    def on_finish(self, total: int):
        print("[{t}/{t}] (100%)".format(t=total))
