from tkinter import BOTH, END, HORIZONTAL, LEFT, RIGHT, TOP, VERTICAL, X, Y, Frame, Label, Listbox, Scrollbar, simpledialog
from typing import List

from copy_to_flash.copier import SourceFile

class ApproveRemoveBeforeDialog(simpledialog.Dialog):
    def __init__(self, master, list: List[SourceFile]) -> None:
        self.__list = list
        super().__init__(master, title='Clear destination before copy')

        
    def body(self, master: Frame):
        self._answer_lbl = Label(master=self, text="Do you want remove next files from flash device before copy?")
        self._answer_lbl.configure(compound='left')

        self.__list_frame_full = Frame(self)
        self.__list_frame_with_x = Frame(self.__list_frame_full)

        self.__scrollbar_y = Scrollbar(self.__list_frame_full, orient=VERTICAL, width=10)
        self.__scrollbar_x = Scrollbar(self.__list_frame_with_x, orient=HORIZONTAL)

        self.__listbox = Listbox(
            master=self.__list_frame_with_x,
            xscrollcommand=self.__scrollbar_x.set, 
            yscrollcommand=self.__scrollbar_y.set,
            width=80,
            height=22,
            state='disabled',
        )
        for f in self.__list.list:
            self.__listbox.insert(END, f.path)

        self.__scrollbar_x.configure(command=self.__listbox.xview)
        self.__scrollbar_y.configure(command=self.__listbox.yview)


        self._answer_lbl.pack(side=TOP, fill=X, expand=True)
        self.__list_frame_full.pack(side=TOP, fill=BOTH, expand=True)
        
        self.__listbox.pack(side=TOP, fill=BOTH, expand=True)
        self.__scrollbar_x.pack(side=TOP, fill=X, expand=True)

        self.__list_frame_with_x.pack(side=LEFT, fill=BOTH, expand=True)
        self.__scrollbar_y.pack(side=RIGHT, fill=Y, expand=True)

        self.geometry("700x500")
        return super().body(master)

