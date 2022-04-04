import os
from glob import glob
from typing import Any

import win32gui

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


def user_select_dir(window_title : str) -> str:
    from PySide6.QtWidgets import QApplication, QFileDialog
    if QApplication.instance():
        app = QApplication.instance()
    else:
        app = QApplication()

    window = QFileDialog()
    window.setFileMode(QFileDialog.Directory)
    window.setWindowTitle(window_title)
    
    select_folder = ""
    if window.exec():
        select_folder = window.selectedFiles()[0]

    return select_folder


def get_window_handle(window_name : str, window_class : str = None) -> list:
    window_handles = list()
    def enum_proc(window_handle : int, param : Any):
        class_name = win32gui.GetClassName(window_handle)
        name = win32gui.GetWindowText(window_handle)

        if window_class and class_name == window_class:
            window_handles.append(window_handle)
        elif window_name and window_name == name:
            window_handles.append(window_handle)

        return True

    win32gui.EnumWindows(enum_proc, tuple())

    return window_handles