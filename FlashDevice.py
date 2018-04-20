class Partition(object):
    def get_mount(self):
        raise NotImplementedError()

    def get_label(self):
        raise NotImplementedError()

    def get_dev_file(self):
        raise NotImplementedError()

    def get_dev_parent(self):
        raise NotImplementedError()


class FlashDevice(object):
    def get_device_file(self):
        raise NotImplementedError()

    def get_partitions(self):
        raise NotImplementedError()

    def get_title(self):
        raise NotImplementedError()
