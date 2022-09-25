import logging
from threading import Lock
from typing import List, Callable, Dict

from multitimer import Multitimer


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


class AvailableDevices(object):
    def __init__(self, getter: Callable[[], List[FlashDevice]]) -> None:
        self.__getter = getter

        self.__lock = Lock()
        self.__label_to_dest_dir: Dict[str, str] = dict()
        self.__choiced_dir = ''
        self.__on_change_available_devices: Callable[[List[str], None]] = None

        self.__check_run_lock = Lock()

        self.__check_available_devices()

        self.__timer = Multitimer(2.0, self.__check_available_devices)
        self.__timer.start()
   
    def set_on_available_devices_changed(self, fn: Callable[[List[str]], None]):
        self.__lock.acquire()
        
        self.__on_change_available_devices = fn
        
        self.__lock.release()

    def set_choiced(self, d):
        self.__lock.acquire()
        
        old = self.__choiced_dir
        self.__choiced_dir = d

        logging.debug('set choiced dir {}. Old {}'.format(d, old))

        self.__check_choiced_partition()
        
        self.__lock.release()

    def get_destination_dir(self):
        self.__lock.acquire()
        
        result = self.__label_to_dest_dir.get(self.__choiced_dir, '')
        
        self.__lock.release()

        return result
    
    def get_available_partitions(self) -> Dict[str, str]:
        self.__lock.acquire()
        
        result = self.__label_to_dest_dir.copy()
        
        self.__lock.release()

        return result

    def get_mounts_labels(self) -> Dict[str, str]:
        self.__lock.acquire()
        
        mounts = []
        for k in self.__label_to_dest_dir:
            mounts.append(k)
        mounts.sort()
        
        self.__lock.release()

        return mounts
    
    def stop_watch(self):
        self.__timer.stop()

    def __check_available_devices(self):
        if self.__check_run_lock.locked():
            logging.info('_check_available_devices already run. Skip current attempt')
            return
        
        logging.debug('running check available devices')

        self.__check_run_lock.acquire()
        self.__lock.acquire()
        
        new_label_to_dest: Dict[str, str] = dict()
        changed = False

        logging.debug('get devices')
        
        for d in self.__getter():
            logging.debug('Pass device {}'.format(d.get_title()))
            for p in d.get_partitions():
                m = p.get_mount()
                l = p.get_label()
                full_label = "{} - {}".format(l, m)
                logging.debug('Pass partition {}'.format(full_label))
                old = self.__label_to_dest_dir.get(full_label, '')
                new_label_to_dest[full_label] = m
                if old != m:
                    changed = True
                    logging.debug('available partition changed, new/changed mount: {}'. format(full_label))
        
        for k in self.__label_to_dest_dir:
            if not new_label_to_dest.get(k):
                changed = True
                logging.debug('mount was deleted: {}'.format(k))
        
        if changed:
            logging.debug("available devices was changed:\nOld:\n{}\n\nNew:\n{}".format(self.__label_to_dest_dir, new_label_to_dest))
            self.__label_to_dest_dir = new_label_to_dest
            self.__check_choiced_partition()
        else:
            logging.debug("available devices was not changed")

        self.__lock.release()

        logging.debug('realise variables lock')

        # running on change outoff lock to prevent deadlock
        # because inside the function can changed this object
        if changed and self.__on_change_available_devices:
            logging.debug('run self._on_change_available_devices')
            self.__on_change_available_devices(self.__label_to_dest_dir.copy())


        self.__check_run_lock.release()

        logging.debug('finish check available devices')

            

    def __check_choiced_partition(self):
        if not self.__label_to_dest_dir.get(self.__choiced_dir):
            old = self.__choiced_dir
            self.__choiced_dir = ''
            logging.warning('choiced dir "{}" is incorrect. It was cleaned'.format(old))
