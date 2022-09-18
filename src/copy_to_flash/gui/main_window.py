import logging
from tkinter import BOTH, LEFT, RIGHT, TOP, X, StringVar, Widget, Variable
from tkinter.filedialog import askdirectory
from tkinter.ttk import LabelFrame, Frame, Entry, Button, Combobox, Label, Progressbar, Spinbox
from typing import List
from gui.widgets import Line
from gui.components import CopierAlgoInput, ProcessOutput
from gui.controller import Controller
from device import FlashDevice


_pad_between_x = 3
_pad_between_y = 10
_pad_between_yy = 5

class MainWindow(Frame):
    def __init__(self, master, controller: Controller): 
        super().__init__(master)

        self._controller = controller        
        self.dir_path = StringVar()
        
        self._build()

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

        parts, selected_part = self._controller.get_available_devices()

        self._desdir_entry_combo = Combobox(self._ddf, values=parts, textvariable=selected_part)
                
        self._desdir_entry_combo.pack(side=LEFT, fill=BOTH, expand=True)
        
        return self._ddf

    def _build_sorter_input(self, parent):
        self._sorter_f = LabelFrame(parent, text='Sorter')

        sorters_list, sorter = self._controller.sorters()

        self._sorter_combo = Combobox(self._sorter_f, values=sorters_list, textvariable=sorter)
        self._sorter_combo.set(sorters_list[0])

        self._sorter_combo.pack(side=LEFT)

        return self._sorter_f

    def _build_input(self, parent):
        input_frame = Frame(parent)

        container = self._build_dest_part_input(input_frame)
        container.pack(side=TOP, fill=X, expand=True, pady=_pad_between_yy)

        container = self._build_source_dir_input(input_frame)
        container.pack(side=TOP, fill=X, expand=True, pady=_pad_between_yy)

        copy_settings = Frame(input_frame)
        container = self._build_sorter_input(copy_settings)
        container.pack(side=LEFT, fill=BOTH, expand=True)
        container = CopierAlgoInput(copy_settings, self._controller)
        container.pack(side=LEFT, fill=BOTH, expand=True)

        copy_settings.pack(side=TOP, fill=X, expand=True, pady=_pad_between_yy)

        self.input_frame = input_frame
        return input_frame

    def _build(self):
        input_frame = self._build_input(self)
        input_frame.pack(side=TOP, fill=X, expand=True, padx=_pad_between_x, pady=_pad_between_y)

        l = Line(self, width=2, color="#E4E4E4")
        l.pack(side=TOP, fill=BOTH, expand=True, padx=_pad_between_x, pady=_pad_between_y)

        self._process = ProcessOutput(self)
        self._process.pack(side=TOP, fill=BOTH, expand=True, padx=_pad_between_x, pady=_pad_between_y)

        self._action_btn = Button(self, text="Start")
        self._action_btn.pack(side=RIGHT, padx=_pad_between_x, pady=(0, _pad_between_y))

        self.pack(side=TOP, fill=X, expand=True)
