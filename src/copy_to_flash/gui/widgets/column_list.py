from tkinter import END, ttk
from typing import Any, Dict, List

class Updatable(object):
    def update(self):
        raise NotImplementedError()

class ListAdapter(object):
    def __init__(self, list: List[Any]) -> None:
        self.list = list
        self.__selected: Any = None
        self.__upd: Updatable = None
    
    def vals(self, o: Any) -> List[str]:
        raise NotImplementedError()

    def columns(self) -> List[str]:
        raise NotImplementedError()

    def swap(self, i: int, j: int):
        if i < 0 or i >= len(self.list):
            raise ValueError("Incorrect first arg")
        
        if j < 0 or j >= len(self.list):
            raise ValueError("Incorrect second arg")
        
        t = self.list[i]
        self.list[i] = self.list[j]
        self.list[j] = t
        if self.__upd:
            self.__upd.update()

    def set_updatable(self, upd: Updatable):
        self.__upd = upd

    def set_selected(self, i: int):
        if i >= len(self.list):
            raise ValueError("Incorrect index")
        
        self.__selected = self.list[i] if i >= 0 else None
    
    def get_selected(self) -> int:
        if not self.__selected:
            return -1

        return self.list.index(self.__selected)
    
    def delete(self, i: int):
        if i < 0 or i >= len(self.list):
            raise ValueError("Incorrect index")
        
        if self.list[i] == self.__selected:
            self.__selected = None

        del self.list[i]
        
        if self.__upd:
            self.__upd.update()


class SingleSelectedColumnList(ttk.Treeview, Updatable):
    def __init__(self, master, list:ListAdapter) -> None:
        self.__adapter = list
        self.__item_indx: Dict[str, int] = dict()

        c_views = self.__adapter.columns()

        indexes = []
        for i in range(len(c_views)):
            indexes.append('#{}'.format(i))

        super().__init__(
            master, 
            show='headings', 
            columns=tuple(indexes),
            selectmode='browse',
        )

        for i in range(len(c_views)):
            self.heading(indexes[i], text=c_views[i], anchor='w')

        self.bind('<<TreeviewSelect>>', self.__on_select)

        self.update()
    
    def update(self):
        self.delete(*self.get_children())
        self.__item_indx = dict()
        selected = self.__adapter.get_selected()
        i = 0
        for f in self.__adapter.list:
            item = self.insert(
                parent="",
                index=END, 
                values=self.__adapter.vals(f)
            )
            self.__item_indx[item] = i
            if i == selected:
                self.selection_set(item)
            i += 1
        

    def __on_select(self, _):
        item = self.selection()
        new_indx = self.__item_indx[item[0]] if item else -1
        self.__adapter.set_selected(new_indx)