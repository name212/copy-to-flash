class NotFoundPartition(Exception):
    pass


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


def __get_partition_from_device(device, choice_part_func):
    parts = device.get_partitions()
    count_parts = len(parts)
    # have one partition - return it
    if count_parts == 1:
        return parts[0]
    # have many parts, choice it
    elif count_parts > 1:
        return choice_part_func(parts)
    # no partition for device (ex no mounted partitions) raise exception
    else:
        raise NotFoundPartition(str(device))


def get_destination_partition(removable_devices, prog_args, choice_part_func):
    # have destination partition. return it
    if prog_args.dest_part:
        return prog_args.dest_part
    # have removable device. show count partitions
    if prog_args.dest_device:
        return __get_partition_from_device(prog_args.dest_device, choice_part_func)

    # not partition or device: user choice from all partitions
    all_parts = []
    for d in removable_devices:
        all_parts += d.get_partitions()
    return choice_part_func(all_parts)