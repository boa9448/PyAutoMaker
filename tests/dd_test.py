import os
import sys

cur_dir = os.path.dirname(__file__)
src_dir = os.path.join(cur_dir, "..", "src")
src_dir = os.path.abspath(src_dir)

sys.path.append(src_dir)

from PyAutoMaker import class_dd

print(class_dd.KEY_LEFT_CTRL)

dd = class_dd.DD()
dd.move(0, 0, False)
dd.key(ord('A'))
dd.key(class_dd.KEY_LEFT_CTRL)