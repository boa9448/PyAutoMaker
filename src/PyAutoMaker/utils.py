import os
from glob import glob

def get_file_list(folder_path : str) -> list:
    return glob(folder_path, recursive = True)

def get_image_file_list(folder_path : str) -> list:
    file_exts = ["png", "jpg", "bmp", "gif"]

    def ext_filter(path : str):
        ext = path.split(os.extsep)[-1].lower()
        if ext in file_exts:
            return True

        return False

    return list(filter(ext_filter, get_file_list(folder_path)))