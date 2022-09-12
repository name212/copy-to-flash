import logging
from tkinter import BOTH, LEFT, RIGHT, TOP, X, StringVar, Widget, Variable
from tkinter.filedialog import askdirectory
from tkinter.ttk import LabelFrame, Frame, Entry, Button, Combobox, Label, Progressbar, Spinbox
from typing import List
from device import FlashDevice

from copier import ProgressTick
from gui.line import Line

_pad_between_x = 3
_pad_between_y = 10
_pad_between_yy = 5

class _Process(LabelFrame):
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
        


class MainWindow(Frame):

    def _on_click_choice_dir(self):
        dir = askdirectory(title='Choice source directory')
        logging.debug('Choicen source dir:{}'.format(dir))
        self.dir_path.set(dir)

    def _build_source_dir_input(self, parent):
        self._sdf = LabelFrame(parent, text='Source directory from copy')

        self._source_dir_entry = Entry(self._sdf, textvariable=self.dir_path)
        
        ask_dir_btn = Button(self._sdf, text='Choice dir...')
        ask_dir_btn.config(command=self._on_click_choice_dir)

        self._source_dir_entry.pack(side=LEFT, fill=BOTH, expand=True)
        ask_dir_btn.pack(side=RIGHT, padx=(_pad_between_x, 0))
        
        return self._sdf

    def _build_dest_part_input(self, parent):
        self._ddf = LabelFrame(parent, text='Destination partition to copy')

        self._desdir_entry_combo = Combobox(self._ddf)
        
        self._desdir_entry_combo.pack(side=LEFT, fill=BOTH, expand=True)
        
        return self._ddf

    def _build_sorter_input(self, parent):
        self._sorter_f = LabelFrame(parent, text='Sorter')

        values=[
            "By title (Asc)"
        ]
        self._sorter_combo = Combobox(self._sorter_f, values=values)
        self._sorter_combo.set(values[0])

        self._sorter_combo.pack(side=LEFT)

        return self._sorter_f

    def _build_copier_input(self, parent):
        self._copier_f = LabelFrame(parent, text='Copier')

        values=[
            "Simple",
            "Limited dir size",
        ]
        self._copier_combo = Combobox(self._copier_f, values=values)
        self._copier_combo.set(values[0])
        self._copier_combo.pack(side=TOP, fill=X, expand=True)

        self._lds_f = Frame(self._copier_f)

        l = Label(self._lds_f, text="Per dir")
        self._per_dir_spin = Spinbox(self._lds_f, from_=1, to=100000)
        self._per_dir_spin.set(512)
        l.pack(side=LEFT, padx=(0, _pad_between_x))
        self._per_dir_spin.pack(side=LEFT)

        self._lds_f.pack(side=TOP, fill=X, expand=True)

        return self._copier_f

    def _build_input(self, parent):
        input_frame = Frame(parent)

        container = self._build_dest_part_input(input_frame)
        container.pack(side=TOP, fill=X, expand=True, pady=_pad_between_yy)

        container = self._build_source_dir_input(input_frame)
        container.pack(side=TOP, fill=X, expand=True, pady=_pad_between_yy)

        copy_settings = Frame(input_frame)
        container = self._build_sorter_input(copy_settings)
        container.pack(side=LEFT, fill=BOTH, expand=True)
        container = self._build_copier_input(copy_settings)
        container.pack(side=LEFT, fill=BOTH, expand=True)

        copy_settings.pack(side=TOP, fill=X, expand=True, pady=_pad_between_yy)

        self.input_frame = input_frame
        return input_frame

    def _build(self):
        input_frame = self._build_input(self)
        input_frame.pack(side=TOP, fill=X, expand=True, padx=_pad_between_x, pady=_pad_between_y)

        l = Line(self, width=2, color="#E4E4E4")
        l.pack(side=TOP, fill=BOTH, expand=True, padx=_pad_between_x, pady=_pad_between_y)

        self._process = _Process(self)
        self._process.pack(side=TOP, fill=BOTH, expand=True, padx=_pad_between_x, pady=_pad_between_y)

        self._action_btn = Button(self, text="Start")
        self._action_btn.pack(side=RIGHT, padx=_pad_between_x, pady=(0, _pad_between_y))

        self.pack(side=TOP, fill=X, expand=True)


    def __init__(self, master): 
        super().__init__(master)
                
        self.dir_path = StringVar()
        
        self._build()