from math import ceil
from tkinter import Canvas

class Line(Canvas):
    def __init__(self, master, cnf={}, width=3, color="black"):
        super().__init__(master, cnf, height=width)

        self._color = color
        self._width = width

        self._func_id = self.bind("<Configure>", self.resize)
    
    def resize(self, event):
        self.delete('all')
        y = ceil(self._width / 2.0)
        self.create_line(0, y, event.width, y, fill=self._color, width=self._width)
