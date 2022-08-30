def show_deleted(path):
    print("Delete {}".format(path), flush=True)


# def show_progress(percent, file_num, count):
#     if percent < 100:
#             print('Copy files ({}):'.format(count), flush=True)
#         print("{}({}/{})".format(percent, file_num, count), end=' ', flush=True)
#     else:
#         print('', flush=True)
#         print('Done!', flush=True)


def show_version(version, on_show):
    print("Version {}".format(version), flush=True)
    on_show()