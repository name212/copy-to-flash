import logging
from tkinter import BOTH, LEFT, RIGHT, TOP, X, StringVar, messagebox
from tkinter.filedialog import askdirectory
from tkinter.ttk import LabelFrame, Frame, Entry, Button, Combobox, Label, Progressbar, Separator, Spinbox
from copier import SourceFile
from gui.dialogs.approve_copy import ApproveBeforeCopyDialog
from gui.components import CopierAlgoInput, ProcessOutput, DestinationPartitionInput
from gui.controller import Controller, FileSourceListAdapter

_pad_between_x = 3
_pad_between_y = 10
_pad_between_yy = 5

class MainWindow(Frame):
    def __init__(self, master, controller: Controller): 
        super().__init__(master)

        self._controller = controller        
        
        self._build()

    def _on_click_choice_dir(self):
        dir = askdirectory(title='Choice source directory')
        logging.debug('Choicen source dir:{}'.format(dir))
        self._controller.source_dir.set(dir)

    def _build_source_dir_input(self, parent):
        self._sdf = LabelFrame(parent, text='Source directory from copy')

        self._source_dir_entry = Entry(self._sdf, textvariable=self._controller.source_dir)
        
        ask_dir_btn = Button(self._sdf, text='Choice dir...')
        ask_dir_btn.config(command=self._on_click_choice_dir)

        self._source_dir_entry.pack(side=LEFT, fill=BOTH, expand=True)
        ask_dir_btn.pack(side=RIGHT, padx=(_pad_between_x, 0))
        
        return self._sdf

    def _build_sorter_input(self, parent):
        self._sorter_f = LabelFrame(parent, text='Sorter')

        sorters_list, sorter = self._controller.sorters()

        self._sorter_combo = Combobox(self._sorter_f, values=sorters_list, textvariable=sorter)
        self._sorter_combo.set(sorters_list[0])

        self._sorter_combo.pack(side=LEFT)

        return self._sorter_f

    def _build_input(self, parent):
        input_frame = Frame(parent)

        self.__available_devices = self._controller.get_available_devices()

        self.__dest_dir_input = DestinationPartitionInput(input_frame, self.__available_devices)
        self.__dest_dir_input.pack(side=TOP, fill=X, expand=True, pady=_pad_between_yy)

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
    
    def __on_start_click(self):
        l = []
        for i in range(1, 200):
            p = "/path/sub/another/dir/suka/hhhhhhhhh/{}".format(i)
            f = SourceFile(p)
            f.attr1 = "Title {}".format(i)
            f.attr2 = "Artist {}".format(i)
            l.append(f)
        dlg = ApproveBeforeCopyDialog(self, FileSourceListAdapter(l))
        
        try:
            self._controller.start_copy()
        except BaseException as e:
            messagebox.showerror("Error", str(e))

    def _build(self):
        input_frame = self._build_input(self)
        input_frame.pack(side=TOP, fill=X, expand=True, padx=_pad_between_x, pady=_pad_between_y)

        l = Separator()
        l.pack(side=TOP, fill=BOTH, expand=True, padx=_pad_between_x, pady=_pad_between_y)

        self._process = ProcessOutput(self)
        self._process.pack(side=TOP, fill=BOTH, expand=True, padx=_pad_between_x, pady=_pad_between_y)

        self._action_btn = Button(self, text="Start", command=self.__on_start_click)
        self._action_btn.pack(side=RIGHT, padx=_pad_between_x, pady=(0, _pad_between_y))

        self.pack(side=TOP, fill=X, expand=True)
