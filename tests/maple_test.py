import os

import cv2

import env
import PyAutoMaker as pam

cur_dir = os.path.dirname(__file__)
imgs_dir = os.path.join(cur_dir, "imgs")
maple = pam.Maple(imgs_dir)
while True:
    try:
        minimap = maple.get_map_img()
        cv2.imshow("map", minimap)
    except KeyboardInterrupt:
        break

    cv2.waitKey(1)

cv2.destroyAllWindows()