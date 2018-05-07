class Arguments(object):
    def get_source(self):
        raise NotImplementedError()

    def get_destination(self):
        raise NotImplementedError()

    def is_verbose(self):
        raise NotImplementedError()
