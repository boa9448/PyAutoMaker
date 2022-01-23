import os
import unittest

import cv2

import env
import PyAutoMaker as pam

class TestMapleModule(unittest.TestCase):
    def __init__(self, methodName: str = ...) -> None:
        self.imgs_dir = env.test_imgs_dir
        self.maple = pam.Maple(self.imgs_dir)
        
        super().__init__(methodName=methodName)

    def test_minimap(self) -> None:
        minimap_img = self.maple.get_map_img()
        self.assertIsNotNone(minimap_img, "미니맵 이미지 가져오기테스트 실패")

    def test_minimap_character(self) -> None:
        char_pt = self.maple.find_char_coordinates()
        self.assertTrue(char_pt)

if __name__ == "__main__":
    unittest.main()