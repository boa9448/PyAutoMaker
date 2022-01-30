import os
import unittest
import subprocess
import time

import cv2
import numpy as np

import env
import PyAutoMaker as pam

class TestImageModule(unittest.TestCase):
    def __init__(self, methodName: str = ...) -> None:
        self.cur_dir = os.path.dirname(__file__)
        self.img_dir = os.path.join(self.cur_dir, "imgs")
        self.src_path = os.path.join(self.img_dir, "src.png")
        self.temp_path = os.path.join(self.img_dir, "temp.png")
        self.temp_mask_path = os.path.join(self.img_dir, "temp2.png")

        super().__init__(methodName=methodName)

    def test_imread(self) -> None:
        src = pam.cv2_imread(self.src_path)
        temp = pam.cv2_imread(self.temp_path)

        self.assertEqual(type(src), np.ndarray)
        self.assertEqual(type(temp), np.ndarray)

    def test_image_search(self) -> None:
        src = pam.cv2_imread(self.src_path)
        temp = pam.cv2_imread(self.temp_path)

        result = pam.imageSearchEx(src, temp)
        self.assertTrue(result)

    def test_image_search_mask(self) -> None:
        src = pam.cv2_imread(self.src_path)
        temp = pam.cv2_imread(self.temp_mask_path)

        result = pam.imageSearchEx(src, temp)
        self.assertTrue(result)

    def test_screenshot(self) -> None:
        notepad = subprocess.Popen(["notepad.exe"])
        time.sleep(1)
        handle = pam.get_window_handle("제목 없음 - Windows 메모장")[0]
        src = pam.screenshot(handle, (0, 0, 100, 100), direct_view = True)
        self.assertEqual(type(src), np.ndarray)

        src = pam.screenshotEx("제목 없음 - Windows 메모장")
        self.assertEqual(type(src), np.ndarray)

        src = pam.desktop_screenshot()
        self.assertEqual(type(src), np.ndarray)

if __name__ == "__main__":
    unittest.main()