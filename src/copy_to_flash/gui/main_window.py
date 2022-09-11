import logging
from tkinter import BOTH, LEFT, RIGHT, TOP, X, StringVar, Widget
from tkinter.filedialog import Directory, FileDialog, askdirectory
from tkinter.ttk import LabelFrame, Frame, Entry, Button, Style

from typing import List
from device import FlashDevice

def pack(w: Widget, side):
    w.pack(side=side)

class MainWindow(Frame):

    def _on_click_choice_dir(self):
        dir = askdirectory(title='Choice source directory')
        logging.debug('Choicen source dir:{}'.format(dir))
        self.dir_path.set(dir)

    def _build_source_dir_input(self):
        self._dpf = LabelFrame(self, text='Source directory from copy')

        self._source_dir_entry = Entry(self._dpf, textvariable=self.dir_path)
        
        ask_dir_btn = Button(self._dpf, text='Choice dir...')
        ask_dir_btn.config(command=self._on_click_choice_dir)

        self._source_dir_entry.pack(side=LEFT, fill=BOTH, expand=True)
        ask_dir_btn.pack(side=RIGHT)
        self._dpf.pack(fill=BOTH, expand=True)

    def _build(self):
        self._build_source_dir_input()
        self.pack(side=TOP, fill=X, expand=True)    


    def __init__(self, master): 
        super().__init__(master)
                
        self.dir_path = StringVar()
        
        self._build()