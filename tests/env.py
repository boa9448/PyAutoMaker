import os
import sys

cur_dir = os.path.dirname(__file__)
src_dir = os.path.join(cur_dir, "..", "src")
src_dir = os.path.abspath(src_dir)

sys.path.append(src_dir)