import logging
from math import ceil
from tkinter import BOTH, LEFT, RIGHT, TOP, X
from tkinter.ttk import LabelFrame, Frame, Combobox, Label, Progressbar, Spinbox
from typing import List
from gui.controller import Controller
from device import FlashDevice

from copier import ProgressTick

pad_between_x = 3

class ProcessOutput(LabelFrame):
    def __init__(self, master) -> None:
        super().__init__(master=master, text="Remove/Copy")
        self._file = Label(self, text='N/A')
        self._progress = Progressbar(self, maximum=100)

        self._file.pack(side=TOP, fill=X, expand=True)
        self._progress.pack(side=TOP, fill=X, expand=True)
    
    def start_copy(self):
        self.configure(text="Copy")
        self._file.configure(text='N/A')
        self._progress.configure(value=0)
    
    def start_clean(self):
        self.configure(text="Remove")
        self._file.configure(text='N/A')
        self._progress.configure(value=0)
    
    def on_process(self, tick: ProgressTick):
        t = tick.file.path
        if tick.file.attr1 and tick.file.attr2:
            t = "{} - {} [{}]".format(tick.file.attr1, tick.file.attr2, t)
        self._file.configure(text=t)
        self._progress.configure(value=tick.percent())
        
class CopierAlgoInput(LabelFrame):
    def __init__(self, master, controller: Controller) -> None:
        super().__init__(master, text="Copier")

        copiers_names, val = controller.copiers()
        self._lds_title = copiers_names[1]

        self._copier_combo = Combobox(self, state="readonly", values=copiers_names, textvariable=val)
        self._copier_combo.set(self._lds_title)
        self._copier_combo.bind('<<ComboboxSelected>>', self.modified)

        self._copier_combo.pack(side=TOP, fill=X, expand=True)

        self._lds_f = Frame(self)

        l = Label(self._lds_f, text="Per dir")
        self._per_dir_spin = Spinbox(self._lds_f, from_=1, to=100000, textvariable=controller.dir_limit_size)
        self._per_dir_spin.set(512)
        l.pack(side=LEFT, padx=(0, pad_between_x))
        self._per_dir_spin.pack(side=LEFT)

        self.show_lsd_input_frame(True)
    
    def modified(self, _):
        cur_val = self._copier_combo.get()
        self.show_lsd_input_frame(self._lds_title == cur_val)
    
    def show_lsd_input_frame(self, is_show):
        if is_show:
            self._lds_f.pack(side=TOP, fill=X, expand=True, after=self._copier_combo)
            logging.debug("Show lds input")
        else: 
            self._lds_f.pack_forget()
            logging.debug("Hide lds input")

    