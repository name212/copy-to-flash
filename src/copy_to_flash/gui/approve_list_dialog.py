import logging
from tkinter import BOTH, BOTTOM, END, HORIZONTAL, LEFT, RIGHT, TOP, VERTICAL, X, Y, Button, Frame, Label, Listbox, Scrollbar, Toplevel, simpledialog, ttk
from turtle import width
from typing import List
from .components import pad_between_y

from copier import SourceFile

class ListAdapter(object):
    def __init__(self, list:List[SourceFile]) -> None:
        self.list = list.copy()
        self.__view = None
        self.selected = ''
    
    def swap(self, i: int, j: int):
        if i < 0 or i >= len(self.list):
            raise ValueError("Incorrect first arg")
        
        if j < 0 or j >= len(self.list):
            raise ValueError("Incorrect second arg")
        
        t = self.list[i]
        self.list[i] = self.list[j]
        self.list[j] = t
        self.__update()

    def delete(self, i: int):
        if i < 0 or i >= len(self.list):
            raise ValueError("Incorrect index")
        del self.list[i]
        self.__update()
    
    def find(self, vv: str) -> int:
        i = 0
        for v in self.list:
            if v.path == vv:
                return i
            i += 1

        return -1
    
    def set_selected(self, s: str):
        self.selected = s
    
    def set_view(self, v: ttk.Treeview):
        self.__view = v
        self.__update()
    
    def __update(self):
        self.__view.delete(*self.__view.get_children())
        for f in self.list:
            i = self.__view.insert(
                parent="",
                index=END, 
                values=[f.attr1, f.attr2, f.path]
            )
            if f.path == self.selected:
                self.__view.selection_set(i)
        

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


class ChageListButtons(Frame):
    def __init__(self, master, list: ListAdapter) -> None:
        super().__init__(master)
        self.__list = list
        
        self.__f = Frame(self)

        self._up_btn = Button(self.__f, text="  Up  ", command=self.__on_up)
        self._up_btn.pack(side=TOP, pady=pad_between_y)

        self._delete_btn = Button(self.__f, text="Delete", command=self.__on_delete)
        self._delete_btn.pack(side=TOP, pady=pad_between_y)

        self._delete_btn = Button(self.__f, text=" Down ", command=self.__on_down)
        self._delete_btn.pack(side=TOP)

        self.__f.pack(side='left')

    def __on_up(self): 
        indx = self.__list.find(self.__list.selected)
        if indx > 0:
            self.__list.swap(indx, indx - 1)
    
    def __on_down(self):
        indx = self.__list.find(self.__list.selected)
        if indx < len(self.__list.list) - 1:
            self.__list.swap(indx, indx + 1)
    
    def __on_delete(self):
        indx = self.__list.find(self.__list.selected)
        if indx >= 0:
            self.__list.delete(indx)



class ApproveBeforeCopyDialog(simpledialog.Dialog):
    def __init__(self, master, list: ListAdapter) -> None:
        self.__list = list
        super().__init__(master, title='Check files before copy')
        
    def body(self, master: Frame):
        self._answer_lbl = Label(master=self, text="Do you want copy next files in next order to flash device?")
        self._answer_lbl.configure(compound='left')

        self.__list_frame_full = Frame(self)
        self.__list_frame_with_x = Frame(self.__list_frame_full)

        self.__scrollbar_y = Scrollbar(self.__list_frame_full, orient=VERTICAL, width=10)
        self.__scrollbar_x = Scrollbar(self.__list_frame_with_x, orient=HORIZONTAL)

        columns = ("#1", "#2", "#3")
        self.__listbox = ttk.Treeview(
            self.__list_frame_with_x, 
            show="headings", 
            columns=columns,
            height=18,
            selectmode='browse',
        )

        self.__listbox.heading("#1", text="Artist", anchor='w')
        self.__listbox.heading("#2", text="Title", anchor='w')
        self.__listbox.heading("#3", text="File", anchor='w')
        self.__listbox.configure(
            yscrollcommand=self.__scrollbar_y.set,
            xscrollcommand=self.__scrollbar_x.set
        )
        self.__scrollbar_x.configure(command=self.__listbox.xview)
        self.__scrollbar_y.configure(command=self.__listbox.yview)

        self.__listbox.column("#1", minwidth=250)
        self.__listbox.column("#2", minwidth=250)
        self.__listbox.column("#3", minwidth=2048)

        self.__list.set_view(self.__listbox)

        self.__action_btns = ChageListButtons(self.__list_frame_full, self.__list)

        self.__listbox.bind('<<TreeviewSelect>>', self.__on_select)

        self._answer_lbl.pack(side=TOP, fill=X, expand=True, anchor='w')
        self.__list_frame_full.pack(side=TOP, fill=BOTH, expand=False)
        
        self.__listbox.pack(side=TOP, fill=BOTH, expand=True)
        self.__scrollbar_x.pack(side=TOP, fill=X, expand=True)

        self.__list_frame_with_x.pack(side=LEFT, fill=BOTH, expand=True)
        self.__scrollbar_y.pack(side=LEFT, fill=Y, expand=True)
        self.__action_btns.pack(side=LEFT, fill=BOTH, expand=True)

        self.geometry("800x500")
        return super().body(master)

    def __on_select(self, _):
        item = self.__listbox.selection()
        if not item:
            self.__list.set_selected('')
            return

        id = item[0]
        v = self.__listbox.item(id)['values'][2]
        logging.debug('select path: {}'.format(v))
        self.__list.set_selected(v)