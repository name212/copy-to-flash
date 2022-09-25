from tkinter import Tk
from typing import List, Callable
from gui.controller import Controller

from device import FlashDevice
from .main.window import MainWindow


class App(Tk):
    def __init__(self, version: str) -> None:
        super().__init__()

        self.title("Copy music to flash")

    def run(self, device_getter: Callable[[], List[FlashDevice]]):
        c = Controller(device_getter=device_getter)
        self.mw = MainWindow(self, controller=c)
        self.mw.mainloop()