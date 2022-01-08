import os
from glob import glob

from PySide6.QtWidgets import QApplication, QFileDialog

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

def user_select_dir() -> str:
    app = QApplication()
    window = QFileDialog()
    window.setFileMode(QFileDialog.Directory)
    
    select_folder = None
    if window.exec():
        select_folder = window.selectedFiles()[0]

    return select_folder