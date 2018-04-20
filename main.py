from pymediainfo import MediaInfo
import os
import platform
import json
from ArgumentParser import parse as parse_argument

_VERSION = "0.0.1"
_EXIT_CODES = {
    'NORMAL': 0
}


def get_available_getter():
    sys = platform.system()
    if sys == "Linux":
        from platforms.LinuxFlashDevice import get_available_devices
        return get_available_devices

    raise Exception("Unsupported platform {}".format(sys))


def filter_path(path):
    info = None
    try:
        info = MediaInfo.parse(path).to_data()
    except BaseException:
        return None
    if not info:
        return None
    name = None
    is_audio = False
    for track in info['tracks']:
        if 'track_type' in track and track['track_type'] == 'Audio':
            is_audio = True
        if 'title' in track and track['title']:
            name = track['title']
    if not name or not is_audio:
        return None

    return {'path': path, 'name': name}


def get_files_list(dir_path):
    paths = []
    all_files_count = 0
    files_count = 0
    for dir_name, dirs, files in os.walk(dir_path, followlinks=True):
        for file in files:
            all_files_count += 1
            path = os.path.join(dir_name, file)
            info = filter_path(path)
            if info:
                paths.append(info)
                files_count += 1
    return paths, all_files_count, files_count


def read_partition_number(count_parts):
    num = None
    count_parts -= 1
    while num is None or num < 0 or num > count_parts:
        num = input("Enter number partition [0 - {}]".format(str(count_parts)))
        try:
            num = int(num)
        except:
            num = None
    return num


def choice_part_console(devices):
    partitions = []
    count_parts = 0
    print("Choice partition:")
    for device in devices:
        print("\t{}".format(str(device)))
        for part in device.get_partitions():
            print("\t\t[{}] - {}".format(count_parts, part))
            partitions.append(part)
            count_parts += 1
    if count_parts == 0:
        print("No found parts")
        raise Exception("No found parts")

    num = read_partition_number(count_parts)
    return partitions[num]


def get_destionation_partition(removable_devices, args, choice_part_func):
    # если имеем конечную партицию то сразу ее возвращаем
    if args.dest_part:
        return args.dest_part
    # если есть устройство (по пути), то смотрим по количеству партиции
    if args.dest_device:
        parts = args.dest_device.get_partitions()
        count_parts = len(parts)
        # если одно то сразу его и возвращаем
        if count_parts == 1:
            return parts[0]
        # если больше одного, то выбираем
        elif count_parts > 1:
            return choice_part_func([args.dest_device])
        # тут нет партиций
        else:
            raise Exception("No found partitions for device " + str(args.dest_device))

    # если нет не партиции и девайса, то выбираем из списка девайсов
    return choice_part_func(removable_devices)


if __name__ == "__main__":
    get_available_devices = get_available_getter()
    removable_devices = get_available_devices()
    args = parse_argument(removable_devices)
    if args.show_version:
        print("Version {}".format(_VERSION))
        exit(_EXIT_CODES['NORMAL'])

    dest = get_destionation_partition(removable_devices, args, choice_part_console)
    print(dest)
