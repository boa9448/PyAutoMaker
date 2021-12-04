import time

from ctypes import Structure, c_byte, c_ubyte, c_uint16

from win32api import GetCursorPos
from serial import Serial

from input_abs import AbsInput


CMD_START_SIGN = c_byte(ord('#'))
CMD_OPCODE_KEY_DATA = 1
CMD_OPCODE_MOUSE_BUTTON = 2
CMD_OPCODE_MOUSE_MOVE = 3

KEY_DATA_STATUS_PRESS = 1
KEY_DATA_STATUS_RELEASE = 2

class CmdHeader(Structure):
    _pack_ = 1
    _fields_ = [("start_sign", c_ubyte)
                , ("opcode", c_uint16)]

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
    _fields_ = [("x", c_byte)
                , ("y", c_byte)]


class ArduinoUtil(AbsInput):
    def __init__(self, port : str, baudrate : int):
        self.serial = Serial(port = port, baudrate = baudrate)

    def __del__(self):
        self.serial.close()

    def key(self, key_code : int, key_status : int):
        header = CmdHeader(CMD_START_SIGN, CMD_OPCODE_KEY_DATA)
        data = KeyData(key_code, key_status)

        data = bytes(header) + bytes(data)
        self.serial.write(data)

    def key_press(self, key_code : int):
        return self.key(key_code, KEY_DATA_STATUS_PRESS)

    def key_release(self, key_code : int):
        return self.key(key_code, KEY_DATA_STATUS_RELEASE)

    def move(self, x : int , y : int, relative : bool) -> bool:
        header = CmdHeader(CMD_START_SIGN, CMD_OPCODE_MOUSE_MOVE)
        cur_x, cur_y = GetCursorPos()
        diff_x, diff_y = cur_x - x, cur_y - y
        if relative:
            pass
        else:
            pass

        self.serial.write(data)

    def btn(self, button_code : int , button_status : int) -> bool:
        pass


if __name__ == "__main__":
    arduino = ArduinoUtil("COM4", 9500)
    packet = arduino.make_packet(KeyData(1, 2))
    print(bytes(packet))
    