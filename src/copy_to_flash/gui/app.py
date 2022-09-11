from tkinter import Tk
from typing import List, Callable

from device import FlashDevice
from .main_window import MainWindow


class App(Tk):
    def __init__(self, version: str) -> None:
        super().__init__()

        self.title("Copy music to flash")
        (width, height) = (500, 450)
        self.geometry("{}x{}".format(width, height))


    def run(self, device_getter: Callable[[], List[FlashDevice]]):
        self.mw = MainWindow(self)
        self.mw.mainloop()