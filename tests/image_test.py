import os

import cv2
import numpy as np

cur_dir = os.path.dirname(__file__)
img_dir = os.path.join(cur_dir, "imgs")
src_path = os.path.join(img_dir, "src.png")
temp_path = os.path.join(img_dir, "temp2.png")

def image_search(src : np.ndarray, temp : np.ndarray, thresh : float, except_color : tuple or None = None):
    mask = ...
    if except_color:
        mask = cv2.inRange(temp, except_color, except_color)
        mask = cv2.bitwise_not(mask)
        mask = cv2.bitwise_and(temp.copy(), cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR))

    result = cv2.matchTemplate(src, temp, cv2.TM_CCORR_NORMED, mask = mask)
    loc = np.where( result >= thresh)

    h, w, c = temp.shape
    rect_list = list()
    for pt in zip(*loc[::-1]):
        start_x, start_y = pt
        end_x, end_y = start_x + w, start_y + h
        rect_list.append((start_x, start_y, end_x, end_y))

    return rect_list


if __name__ == "__main__":
    src = cv2.imread(src_path, cv2.IMREAD_UNCHANGED)
    temp = cv2.imread(temp_path, cv2.IMREAD_UNCHANGED)
    rects = image_search(src, temp, 1.0, (0, 0, 255))
    print(rects)