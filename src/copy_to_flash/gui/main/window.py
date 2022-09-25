import logging
from tkinter import BOTH, LEFT, RIGHT, TOP, X
from tkinter.ttk import LabelFrame, Frame, Entry, Button, Combobox, Separator
from gui.handlers import GUIClearHandler, GUICopyHandler, Window
from gui.main.components import CopierAlgoInput, ProcessOutput, DestinationPartitionInput, SourceDirInput
from gui.controller import Controller

_pad_between_x = 3
_pad_between_y = 10
_pad_between_yy = 5

class MainWindow(Frame, Window):
    def __init__(self, master, controller: Controller): 
        super().__init__(master)

        self._controller = controller
        self._controller.set_clear_handler(GUIClearHandler(self))
        self._controller.set_copy_handler(GUICopyHandler(self))        
        
        self._build()

    def _build_sorter_input(self, parent):
        self._sorter_f = LabelFrame(parent, text='Sorter')

        sorters_list, sorter = self._controller.sorters()

        self._sorter_combo = Combobox(self._sorter_f, values=sorters_list, textvariable=sorter)
        self._sorter_combo.set(sorters_list[0])

        self._sorter_combo.pack(side=LEFT)

        return self._sorter_f

    def _build_input(self, parent):
        input_frame = Frame(parent)

        self.__source_dir_input = SourceDirInput(input_frame, self._controller.source_dir)
        self.__source_dir_input.pack(side=TOP, fill=X, expand=True, pady=_pad_between_yy)

        self.__available_devices = self._controller.get_available_devices()
                
        self.__dest_dir_input = DestinationPartitionInput(input_frame, self.__available_devices)
        self.__dest_dir_input.pack(side=TOP, fill=X, expand=True, pady=_pad_between_yy)

        copy_settings = Frame(input_frame)
        container = self._build_sorter_input(copy_settings)
        container.pack(side=LEFT, fill=BOTH, expand=True)
        self.__copier_input = CopierAlgoInput(copy_settings, self._controller)
        self.__copier_input.pack(side=LEFT, fill=BOTH, expand=True)

        copy_settings.pack(side=TOP, fill=X, expand=True, pady=_pad_between_yy)

        self.input_frame = input_frame
        return input_frame
    
    def _build(self):
        input_frame = self._build_input(self)
        input_frame.pack(side=TOP, fill=X, expand=True, padx=_pad_between_x, pady=_pad_between_y)

        l = Separator(self)
        l.pack(side=TOP, fill=BOTH, expand=True, padx=_pad_between_x, pady=_pad_between_y)

        self.process = ProcessOutput(self)
        self.process.pack(side=TOP, fill=BOTH, expand=True, padx=_pad_between_x, pady=_pad_between_y)

        self._action_btn = Button(self)
        self.switch_to_start()
        self._action_btn.pack(side=RIGHT, padx=_pad_between_x, pady=(0, _pad_between_y))

        self.pack(side=TOP, fill=X, expand=True)

    def switch_to_cancel(self):
        self._action_btn.configure(
            text="Cancel",
            command=self._controller.cancel
        )

        self.__dest_dir_input.readonly(True)
        self.__source_dir_input.readonly(True)
        self.__copier_input.readonly(True)
        self._sorter_combo.configure(state='disabled')
    
    def switch_to_start(self):
        self.process.reset()
        self._action_btn.configure(
            text="Start",
            command=self._controller.start_copy
        )

        self.__dest_dir_input.readonly(False)
        self.__source_dir_input.readonly(False)
        self.__copier_input.readonly(False)
        self._sorter_combo.configure(state='readonly')
    
    def get_process(self) -> ProcessOutput:
        return self.process
    
    def run_after(self, ms: int, fun):
        self.after(ms, fun)
