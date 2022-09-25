import logging
from tkinter import simpledialog

class OkCancelDialog(simpledialog.Dialog):
    def __init__(self, parent, title: str) -> None:
        self.result = False
        super().__init__(parent, title)
    
    def ok(self, event = None) -> None:
        self.result = True
        return super().ok(event)
