import json
import logging
from subprocess import check_output
from typing import List

from device import FlashDevice, Partition


class __LinuxPartition(Partition):
    def __init__(self, parent, name=None, mount=None, label=None, size=None):
        """
        :type parent: __LinuxFlashDevice
        :param str mount:
        :param str name:
        :param str label:
        """
        if not mount:
            raise Exception("Incorrect mount")
        if not name:
            raise Exception("Incorrect name")
        if not label:
            label = 'N/A'
        self.__parent = parent
        self.__mount = mount
        self.__label = label
        self.__name = name
        self.__size = size

    def get_mount(self):
        return self.__mount

    def get_label(self):
        return self.__label

    def get_dev_file(self):
        return '/dev/' + self.__name

    def get_dev_parent(self):
        return self.__parent


class __LinuxFlashDevice(FlashDevice):
    def __init__(self, name=None, partitions=None, vendor=None, model=None):
        """
        :param str name:
        :param list partitions:
        :param str vendor:
        :param str model:
        """
        if not name:
            raise Exception("Not name for device")

        self.__name = name
        self.__partitions = partitions
        self.__vendor = vendor
        self.__model = model

    def get_partitions(self):
        return self.__partitions

    def get_title(self):
        if self.__model and self.__vendor:
            return self.__model + self.__vendor
        elif self.__model:
            return self.__model
        elif self.__vendor:
            return self.__vendor

        return 'N/A'

    def get_dev_file(self):
        return '/dev/' + self.__name


def __get_block_devices():
    """
    :rtype: dict
    """
    out = check_output(args=["lsblk",
                             "-J",
                             "--output=NAME,VENDOR,MODEL,MOUNTPOINT,LABEL,STATE,RM,TYPE,SIZE"],
                       )
    devices = json.loads(out.decode())
    if "blockdevices" in devices:
        return devices['blockdevices']

    raise Exception("Not found block devices")


def __build_device(device: dict) -> FlashDevice:
    partitions = []
    flash_device = __LinuxFlashDevice(name=device.get('name'),
                                      partitions=partitions,
                                      model=device.get('model'),
                                      vendor=device.get('vendor'))
    if "children" in device:
        for child in device['children']:
            if "type" in child and child['type'] == "part":
                part = __LinuxPartition(parent=flash_device,
                                        name=child.get('name'),
                                        mount=child.get('mountpoint'),
                                        label=child.get('label'),
                                        size=child.get('size'))
                partitions.append(part)

    return flash_device


def get_available_devices() -> List[FlashDevice]:
    block_devices = __get_block_devices()
    available_devices = []
    for device in block_devices:
        removable = device.get("rm")
        type_dev = device.get("type")
        if not type_dev or type_dev != "disk" or not removable:
            continue
        available_devices.append(__build_device(device))
    return available_devices
