from typing import List

from ..device import FlashDevice, Partition


class NotFoundPartition(Exception):
    pass

def read_yes_no() -> bool:
    while True :
        a = input("y/n:")
        a = a.lower()
        if a == "y":
            return True
        elif a == "n":
           return False

def __read_partition_number(count_parts: int) -> int:
    num = None
    count_parts -= 1
    while num is None or num < 0 or num > count_parts:
        num = input("Enter number partition [0 - {}]:".format(str(count_parts)))
        try:
            num = int(num)
        except TypeError:
            num = None
    return num


def __show_available_parts(parts: List[Partition]) -> List[Partition]:
    device_grouped_parts = {}
    for part in parts:
        device = part.get_dev_parent()
        dev_file = device.get_dev_file()
        list_on_device = device_grouped_parts.get(dev_file, {'dev': device, 'parts': []})
        list_on_device['parts'].append(part)
        device_grouped_parts[dev_file] = list_on_device

    count_part = 0
    sorted_parts = []
    print("Choice partition:")
    for device_file in sorted(device_grouped_parts):
        device = device_grouped_parts[device_file]
        print("{}".format(str(device['dev'])))
        for part in device['parts']:
            print("\t[{}] - {}".format(count_part, part))
            sorted_parts.append(part)
            count_part += 1
    return sorted_parts


def choice_dest_partition(partitions: List[Partition]) -> Partition:
    count_parts = len(partitions)
    if count_parts == 0:
        print("No found parts")
        raise Exception("No found parts")
    ordered_parts = __show_available_parts(partitions)
    num = __read_partition_number(len(ordered_parts))
    return ordered_parts[num]


def get_partition_from_device(device: FlashDevice) -> Partition:
    parts = device.get_partitions()
    count_parts = len(parts)
    # have one partition - return it
    if count_parts == 1:
        return parts[0]
    # have many parts, choice it
    elif count_parts > 1:
        return choice_dest_partition(parts)
    # no partition for device (ex no mounted partitions) raise exception
    else:
        raise NotFoundPartition(str(device))

