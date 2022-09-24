import logging
from tkinter import messagebox
from typing import List

from copier import CleanHandler, CopyHandler, ProgressTick, SourceFile
from gui.widgets.column_list import ListAdapter
from gui.dialogs.approve_copy import ApproveBeforeCopyDialog
from gui.dialogs.approve_remove import ApproveRemoveBeforeDialog
from gui.main_window import MainWindow


class FileSourceListAdapter(ListAdapter):
    def __init__(self, list: List[SourceFile]) -> None:
        super().__init__(list)

    def vals(self, o: SourceFile) -> List[str]:
        return [o.attr1, o.attr2, o.path]

    def columns(self) -> List[str]:
        return ["Title", "Artist", "File"]


class GUIClearHandler(CleanHandler):
    def __init__(self, window: MainWindow) -> None:
        super().__init__()
        self.__window = window

    def on_before_clear(self, files: List[SourceFile]) -> bool:
        dlg = ApproveRemoveBeforeDialog(self.__window, files)
        
        if dlg.result:
            self.__window.process.start_clean()
        else:
            messagebox.showinfo('Copying has been canceled. Device should be cleaned before.')
            self.__window.process.reset()
        
        return dlg.result
    
    def on_process(self, tick: ProgressTick):
        self.__window.process.on_process(tick)

    def on_finish(self, total: int):
        pass


class GUIHandler(CopyHandler):
    def __init__(self, window: MainWindow) -> None:
        super().__init__()
        self.__window = window
    
    def on_before_copy(self, files: List[SourceFile]) -> List[SourceFile]:
        adapter = FileSourceListAdapter(files)
        dlg = ApproveBeforeCopyDialog(self.__window, adapter)
        
        if dlg.result:
            self.__window.process.start_copy()
            return adapter.list 
        else:
            self.__window.process.reset()

    def on_process(self, tick: ProgressTick):
        self.__window.process.on_process(tick)
    
    def on_finish(self, total: int):
        messagebox.showinfo('Copying has been finished.')
        self.__window.process.reset()

