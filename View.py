class View(object):
    def show_version(self, version, on_showed):
        raise NotImplementedError()

    def show_progress(self, percent, file_num, count):
        raise NotImplementedError()

    def show_deleted(self, path):
        raise NotImplementedError()
