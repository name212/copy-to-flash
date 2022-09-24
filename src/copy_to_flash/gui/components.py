import logging
from tkinter import BOTH, LEFT, TOP, X
from tkinter.ttk import LabelFrame, Frame, Combobox, Label, Progressbar, Spinbox
from typing import Dict, List
from gui.controller import Controller
from device import AvailableDevices

from copier import ProgressTick

pad_between_x = 3
pad_between_y = 5

class ProcessOutput(LabelFrame):
    def __init__(self, master) -> None:
        super().__init__(master=master)
        self._file = Label(self, text='N/A')
        self._progress = Progressbar(self, maximum=100)

        self.reset()

        self._file.pack(side=TOP, fill=X, expand=True)
        self._progress.pack(side=TOP, fill=X, expand=True)
    
    def reset(self):
        self.configure(text="Remove/Copy")
        self._file.configure(text='N/A')
        self._progress.configure(value=0)

    def start_copy(self):
        self.configure(text="Copying")
        self._file.configure(text='N/A')
        self._progress.configure(value=0)
    
    def start_clean(self):
        self.configure(text="Removing")
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

class DestinationPartitionInput(LabelFrame):
    def __init__(self, master, available_devices: AvailableDevices) -> None:
        super().__init__(master, text='Destination partition to copy')

        self.__logger = logging.getLogger(__name__)
        
        self.__available_devices = available_devices

        self.__desdir_entry_combo = Combobox(self, state="readonly")

        self.__on_available_devices_changed(self.__available_devices.get_available_partitions())

        available_devices.set_on_available_devices_changed(self.__on_available_devices_changed)
        self.__desdir_entry_combo.bind('<<ComboboxSelected>>', self.__modified)
                
        self.__desdir_entry_combo.pack(side=LEFT, fill=BOTH, expand=True)

    def __modified(self, _):
        self.__available_devices.set_choiced(self.__desdir_entry_combo.get())

    def __on_available_devices_changed(self, devices: Dict[str, str]):
        self.__logger.debug('__on_available_devices_changed run: {}'.format(devices))

        cur_val = self.__desdir_entry_combo.get()
        
        mount: List[str] = []
        found = False
        for k in devices:
            if k == cur_val:
                found = True
            mount.append(k)
        mount.sort()

        if len(mount) == 0:
            mount.append('Not found devices. Plug-in USB device')
        if not found:
            cur_val = mount[0]

        self.__desdir_entry_combo.configure(values=mount)
        self.__desdir_entry_combo.set(cur_val)
    
    def destroy(self) -> None:
        self.__available_devices.stop_watch()
        return super().destroy()
