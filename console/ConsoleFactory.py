from InterfaceFactory import InterfaceFactory
from Controller import Controller
from View import View


class _ConsoleView(View):
    def show_version(self, version, on_show):
        print("Version {}".format(version))
        on_show()


class _ConsoleController(Controller):
    def __init__(self, view):
        self.__view = view

    def choice_dest_partition(self, partitions):
        count_parts = len(partitions)
        if count_parts == 0:
            print("No found parts")
            raise Exception("No found parts")
        ordered_parts = self.__show_available_parts(partitions)
        num = self.__read_partition_number(len(ordered_parts))
        return ordered_parts[num]

    @staticmethod
    def __read_partition_number(count_parts):
        num = None
        count_parts -= 1
        while num is None or num < 0 or num > count_parts:
            num = input("Enter number partition [0 - {}]:".format(str(count_parts)))
            try:
                num = int(num)
            except TypeError:
                num = None
        return num

    @staticmethod
    def __show_available_parts(parts):
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


class ConsoleFactory(InterfaceFactory):
    def __init__(self):
        self.__view = _ConsoleView()
        self.__controller = _ConsoleController(self.__view)

    def get_view(self):
        return self.__view

    def get_controller(self):
        return self.__controller
