import os

def check_is_dir_exists(dir: str):
    if not os.path.exists(dir) or not os.path.isdir(dir):
        raise Exception("{} is not dir".format(dir))
        