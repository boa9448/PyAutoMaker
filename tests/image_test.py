import os
import unittest

import cv2
import numpy as np

import env
import PyAutoMaker as pam

class TestImageModule(unittest.TestCase):
    def setUp(self) -> None:
        self.cur_dir = os.path.dirname(__file__)
        self.img_dir = os.path.join(self.cur_dir, "imgs")
        self.src_path = os.path.join(self.img_dir, "src.png")
        self.temp_path = os.path.join(self.img_dir, "temp.png")
        self.temp_mask_path = os.path.join(self.img_dir, "temp2.png")

        return super().setUp()

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


if __name__ == "__main__":
    unittest.main()