import sys
import os
from os.path import dirname

root_dir = dirname(__file__)

sys.path.append(root_dir)
os.environ["PATH"] += os.pathsep + os.path.join(root_dir, "dlls")
os.environ["DLL_FOLDER"] = os.path.join(root_dir, "dlls")
os.environ["DNN_DATA_FOLDER"] = os.path.join(root_dir, "models")
os.environ["IMG_DATA_FOLDER"] = os.path.join(root_dir, "imgs")

from . import darknet
from . import image
from . import arduino
from . import class_dd
from . import input
from . import maple
from . import utils
from . import exception