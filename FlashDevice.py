class Partition(object):
    def get_mount(self):
        raise NotImplementedError()

    def get_label(self):
        raise NotImplementedError()

    def get_dev_file(self):
        raise NotImplementedError()

    def get_dev_parent(self):
        raise NotImplementedError()

    def __str__(self):
        return 'Partition {} with label "{}" mounted in {}'.format(
            self.get_dev_file(),
            self.get_label(), self.get_mount())


class FlashDevice(object):
    def get_dev_file(self):
        raise NotImplementedError()

    def get_partitions(self):
        raise NotImplementedError()

    def get_title(self):
        raise NotImplementedError()

    def __str__(self):
        return "Device {} {}".format(self.get_dev_file(), self.get_title())
