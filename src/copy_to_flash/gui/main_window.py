from curses.panel import top_panel
import logging
from tkinter import BOTH, LEFT, RIGHT, TOP, X, StringVar, Widget, Variable
from tkinter.filedialog import askdirectory
from tkinter.ttk import LabelFrame, Frame, Entry, Button, Combobox, Label, Spinbox

from typing import List
from device import FlashDevice

def pack(w: Widget, side):
    w.pack(side=side)

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
        ask_dir_btn.pack(side=RIGHT, padx=(3, 0))
        
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
        l.pack(side=LEFT)
        self._per_dir_spin.pack(side=LEFT)

        self._lds_f.pack(side=TOP, fill=X, expand=True)

        return self._copier_f

    def _build_input(self, parent):
        input_frame = Frame(parent)

        container = self._build_dest_part_input(input_frame)
        container.pack(side=TOP, fill=X, expand=True)

        container = self._build_source_dir_input(input_frame)
        container.pack(side=TOP, fill=X, expand=True)

        copy_settings = Frame(input_frame)
        container = self._build_sorter_input(copy_settings)
        container.pack(side=LEFT, fill=BOTH, expand=True)
        container = self._build_copier_input(copy_settings)
        container.pack(side=LEFT, fill=BOTH, expand=True)
        copy_settings.pack(side=TOP, fill=X, expand=True)

        self.input_frame = input_frame
        return input_frame


    def _build(self):
        input_frame = self._build_input(self)
        input_frame.pack(side=TOP, fill=X, expand=True)

        self.pack(side=TOP, fill=X, expand=True)


    def __init__(self, master): 
        super().__init__(master)
                
        self.dir_path = StringVar()
        
        self._build()