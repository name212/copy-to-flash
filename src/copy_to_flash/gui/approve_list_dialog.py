from tkinter import BOTH, END, HORIZONTAL, LEFT, RIGHT, TOP, VERTICAL, X, Y, Frame, Label, Listbox, Scrollbar, simpledialog
from typing import List

from copier import SourceFile

class ListAdapter(object):
    def __init__(self, list:List[SourceFile]) -> None:
        self.list = list.copy()
    
    def swap(self, i: int, j: int):
        if i < 0 or i >= len(self.list):
            raise ValueError("Incorrect first arg")
        
        if j < 0 or j >= len(self.list):
            raise ValueError("Incorrect second arg")
        
        t = self.list[i]
        self.list[i] = self[j]
        self.list[j] = t

    def delete(self, i: int):
        if i < 0 or i >= len(self.list):
            raise ValueError("Incorrect index")
        del self.list[i]

class ApproveRemoveBeforeDialog(simpledialog.Dialog):
    def __init__(self, master, list: ListAdapter) -> None:
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