class InterfaceFactory(object):
    def get_view(self):
        raise NotImplementedError()

    def get_controller(self):
        raise NotImplementedError()
