from input_abs import *
from arduino import ArduinoUtil
from class_dd import DDUtil

class InputUtil:
    def __init__(self, backend : ArduinoUtil or DDUtil, args : tuple):
        self.backend = backend(*args)

    def key(self, key_code : int, key_status : int):
        return self.backend.key(key_code, key_status)

    def move(self, x : int , y : int, relative : bool):
        return self.backend.move(x, y, relative)

    def btn(self, button_code : int , button_status : int):
        return self.backend.btn(button_code, button_status)

