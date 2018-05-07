class PathFilter(object):
    def process_path(self, path):
        raise NotImplementedError()

    def get_sort_paths_list(self):
        raise NotImplementedError()
