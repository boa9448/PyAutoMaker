import random
import time
from threading import Event
from queue import Queue

import mouse
import win32api
import win32con

from input_abs import *
from arduino import ArduinoUtil
from class_dd import DDUtil

class InputUtil:
    def __init__(self, backend : ArduinoUtil or DDUtil, args : tuple) -> None:
        self.backend = backend(*args)

    def key(self, key_code : int, key_status : int) -> None:
        return self.backend.key(key_code, key_status)

    def key_press(self, key_code : int) -> None:
        return self.backend.key_press(key_code)

    def key_release(self, key_code : int) -> None:
        return self.backend.key_release(key_code)

    def move(self, x : int , y : int, relative : bool) -> None:
        return self.backend.move(x, y, relative)

    def btn(self, button_code : int , button_status : int) -> None:
        return self.backend.btn(button_code, button_status)


if __name__ == "__main__":
    pass
