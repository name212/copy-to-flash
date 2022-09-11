from tkinter import Tk
from typing import List

from device import FlashDevice
from .main_window import MainWindow


class App(Tk):
    def __init__(self) -> None:
        super().__init__()

        self.title("Copy music to flash")
        (width, height) = (500, 450)
        self.geometry("{}x{}".format(width, height))


    def run(self, available_devices: List[FlashDevice], version: str):
        self.mw = MainWindow(self)
        self.mw.mainloop()