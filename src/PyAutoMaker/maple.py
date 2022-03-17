import os
import time
from typing import Callable

import cv2
import numpy as np

from . import image

def time_check(func) -> Callable:
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        print(f"{func.__name__} : {time.time() - start:.2f}")
        return result

    return wrapper

class MiniMapNotFound(Exception):
    def __init__(self, message):
        super().__init__(message)

class Maple:
    def __init__(self, img_folder_path : str):
        self.imgs = image.cv2_imreads(img_folder_path)
        self.src = self.imgs["maple_src.png"]
        self.map_char_img = self.imgs["maple_map_character.png"]
        self.map_left_top_img = self.imgs["maple_map_start_mask.png"]
        self.map_right_bottom_img = self.imgs["maple_map_end_mask.png"]

        self.minimap_left_top = tuple()
        self.minimap_right_bottm = tuple()

    def __dell__(self):
        pass

    @time_check
    def screen_shot(self) -> np.ndarray:
        return image.screenshotEx("MapleStory")

    @time_check
    def find_map_coordinates(self, screen_shot : np.ndarray or None = None) -> tuple:
        if self.minimap_left_top and self.minimap_right_bottm:
            return (*self.minimap_left_top, *self.minimap_right_bottm)

        if screen_shot is None:
            screen_shot = self.screen_shot()

        left, top = image.imageSearchEx(screen_shot, self.map_left_top_img, (255, 0, 0), False)[:2]
        right, bottom = image.imageSearchEx(screen_shot, self.map_right_bottom_img, (255, 0, 0), False)[2:]
        
        self.minimap_left_top = (left, top)
        self.minimap_right_bottm = (right, bottom)

        return left, top, right, bottom

    @time_check
    def get_map_img(self) -> np.ndarray:
        screen_shot = self.screen_shot()
        left, top, right, bottom = self.find_map_coordinates(screen_shot)
        return screen_shot[top : bottom, left : right].copy()

    @time_check
    def find_char_coordinates(self, screen_shot : np.ndarray or None = None) -> tuple:
        if screen_shot is None:
            screen_shot = self.get_map_img()

        result = image.imageSearchEx(screen_shot, self.map_char_img, (255, 0, 0), False)
        if not result:
            return tuple()

        left, top, right, bottom = result
        width, height = right - left, bottom - top
        center_x = left + int(width / 2)
        center_y = top + int(height / 2)

        return center_x, center_y
        

if __name__ == "__main__":
    pass

