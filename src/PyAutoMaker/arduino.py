import time
from ctypes import POINTER, Structure, Union, byref, c_byte, c_short, c_ushort, memmove, pointer, sizeof, cast

from serial import Serial

from input_abs import AbsInput

class KeyData(Structure):
    _pack_ = 1
    _fields_ = [("key_code", c_byte)
                , ("key_status", c_byte)]


class MouseButtonData(Structure):
    _pack_ = 1
    _fields_ = [("button_code", c_byte)
                , ("button_status", c_byte)]


class MouseMoveData(Structure):
    _pack_ = 1
    _fields_ = [("move_type", c_byte)
                ,("move_mode", c_byte)
                , ("x", c_short)
                , ("y", c_short)]


class ArduinoUtil(AbsInput):
    START_SIGN = c_byte(ord('#'))
    DATA_TYPE = {KeyData : c_byte(1), MouseButtonData : c_byte(2), MouseMoveData : c_byte(3)}

    def __init__(self, port : str, baudrate : int):
        #self.serial = Serial(port = port, baudrate = baudrate)
        pass

    def __del__(self):
        #self.serial.close()
        pass

    def make_packet(self, data : KeyData or MouseButtonData or MouseMoveData) -> bytes:
        packet = bytes(self.START_SIGN) + bytes(self.DATA_TYPE[type(data)]) + bytes(data)
        return packet

    def key(self, key_code : int, key_status : int) -> bool:
        pass

    def move(self, mode : int, x : int , y : int) -> bool:
        pass

    def btn(self, button_code : int , button_status : int) -> bool:
        pass


if __name__ == "__main__":
    arduino = ArduinoUtil("COM4", 9500)
    packet = arduino.make_packet(KeyData(1, 2))
    print(bytes(packet))
    