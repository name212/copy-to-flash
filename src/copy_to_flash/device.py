from typing import List

class NotFoundPartition(Exception):
    pass


class Partition(object):
    def get_mount(self) -> str:
        raise NotImplementedError()

    def get_label(self) -> str:
        raise NotImplementedError()

    def get_dev_file(self) -> str:
        raise NotImplementedError()

    def get_dev_parent(self) -> "FlashDevice":
        raise NotImplementedError()

    def __str__(self):
        return 'Partition {} with label "{}" mounted in {}'.format(
            self.get_dev_file(),
            self.get_label(), self.get_mount())


class FlashDevice(object):
    def get_dev_file(self) -> str:
        raise NotImplementedError()

    def get_partitions(self) -> List[Partition]:
        raise NotImplementedError()

    def get_title(self) -> str:
        raise NotImplementedError()

    def __str__(self):
        return "Device {} {}".format(self.get_dev_file(), self.get_title())

