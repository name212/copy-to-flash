from typing import List

from src.copy_to_flash.console.input import read_yes_no

from ..copier import CleanHandler, ProgressTick


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

    def on_finish(self):
        if self.verbose:
            print("Destination device was cleaned")