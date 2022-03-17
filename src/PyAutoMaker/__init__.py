import sys
import os
from os.path import dirname, abspath

root_dir = abspath(dirname(__file__))

os.add_dll_directory(os.path.join(root_dir, "dlls"))
dll_folder = os.path.join(root_dir, "dlls")
dnn_data_folder = os.path.join(root_dir, "models")
img_data_folder = os.path.join(root_dir, "imgs")

from . import darknet
from . import image
from . import arduino
from . import class_dd
from . import input
from . import maple
from . import utils
from . import exception