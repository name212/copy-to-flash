from queue import Queue
from tkinter import messagebox
from typing import List

from copier import CleanHandler, CopyHandler, ProgressTick, SourceFile
from gui.widgets.column_list import ListAdapter
from gui.dialogs.approve_copy import ApproveBeforeCopyDialog
from gui.dialogs.approve_remove import ApproveRemoveBeforeDialog
from gui.main.components import ProcessOutput

class Window(object):
    def get_process(self) -> ProcessOutput:
        raise NotImplementedError()
    
    def switch_to_start(self):
        raise NotImplementedError()
    
    def switch_to_cancel(self):
        raise NotImplementedError()

    def run_after(self, ms: int, fun):
        raise NotImplementedError()


class FileSourceListAdapter(ListAdapter):
    def __init__(self, list: List[SourceFile]) -> None:
        super().__init__(list)

    def vals(self, o: SourceFile) -> List[str]:
        return [o.attr1, o.attr2, o.path]

    def columns(self) -> List[str]:
        return ["Title", "Artist", "File"]


class GUIClearHandler(CleanHandler):
    def __init__(self, window: Window) -> None:
        super().__init__()
        self.__window = window

    def on_before_clear(self, files: List[SourceFile]) -> bool:
        q = Queue(1)
        def run(q: Queue):
            dlg = ApproveRemoveBeforeDialog(self.__window, files)
            if dlg.result:
                self.__window.get_process().start_clean()
            else:
                messagebox.showinfo(title='Canceled', message='Copying has been canceled. Device should be cleaned before.')
                self.__window.switch_to_start()
            q.put(dlg.result)
        
        self.__window.run_after(250, lambda: run(q))
        
        return q.get()
    
    def on_process(self, tick: ProgressTick):
        self.__window.get_process().on_process(tick)

    def on_finish(self, total: int):
        t = ProgressTick(SourceFile(''), file_index=1, total_files=1)
        self.__window.get_process().on_process(t)


class GUICopyHandler(CopyHandler):
    def __init__(self, window: Window) -> None:
        super().__init__()
        self.__window = window
    
    def on_before_copy(self, files: List[SourceFile]) -> List[SourceFile]:
        self.__window.get_process().wait_finish()

        q = Queue(1)
        def run(q: Queue):
            adapter = FileSourceListAdapter(files)
            dlg = ApproveBeforeCopyDialog(self.__window, adapter)

            if dlg.result:
                self.__window.get_process().start_copy()
                self.__window.switch_to_cancel()
                q.put(adapter.list) 
            else:
                self.__window.switch_to_start()
                q.put([])
        
        self.__window.run_after(250, lambda: run(q))
        
        return q.get()


    def on_process(self, tick: ProgressTick):
        self.__window.get_process().on_process(tick)
    
    def on_finish(self, total: int):
        t = ProgressTick(SourceFile(''), file_index=total, total_files=total)
        self.__window.get_process().on_process(t)

        self.__window.get_process().wait_finish()

        def run():    
            messagebox.showinfo(title='Done', message='Copying has been finished.')
            self.__window.switch_to_start()
        
        self.__window.run_after(1000, run)


