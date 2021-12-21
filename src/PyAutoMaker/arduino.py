import os
import time
from ctypes import Structure, c_byte, c_ubyte, c_uint16

from win32api import GetCursorPos
from serial import Serial
from serial.tools import list_ports

from input_abs import *
from arduino_define import *

def get_port_list(name = "USB 직렬 장치") -> list:
    find_port_list = list_ports.comports()
    port_list = list()
    for port in find_port_list:
        if name in port.description:
            port_list.append(port.device)

    return port_list

def upload(port : str, arduino_dir : str = "C:\\Program Files (x86)\\Arduino") -> bool:
    os.environ["path"] = os.pathsep.join([os.environ["path"], arduino_dir])
    cur_dir = os.path.dirname(__file__)
    src_path = os.path.abspath(os.path.join(cur_dir, "arduino_keyboard_src", "arduino_keyboard_src.ino"))
    upload_command = f"arduino_debug.exe --board arduino:avr:leonardo --port {port} --upload {src_path}"

    ret_code = os.system(upload_command)
    return True if ret_code == 0 else False

class ArduinoUtil(AbsInput):
    MOVE_STEP = 100

    def __init__(self, port : str, baudrate : int):
        self.serial = Serial(port = port, baudrate = baudrate)
        time.sleep(2)

    def __del__(self):
        self.serial.close()

    def key(self, key_code : int):
        self.key_press(key_code)
        self.key_release(key_code)

    def key_press(self, key_code : int):
        header = CmdHeader(CMD_START_SIGN, CMD_OPCODE_KEY_DATA)
        data = KeyData(arduino_key_map.get(key_code, key_code), ARDUINO_KEY_PRESS)

        data = bytes(header) + bytes(data)
        self.serial.write(data)

    def key_release(self, key_code : int):
        header = CmdHeader(CMD_START_SIGN, CMD_OPCODE_KEY_DATA)
        data = KeyData(arduino_key_map.get(key_code, key_code), ARDUINO_KEY_RELEASE)

        data = bytes(header) + bytes(data)
        self.serial.write(data)

    def string(self, s : str):
        for c in s:
            self.key(ord(c))
            time.sleep(0.03)

    def make_move_data(self, x : int , y : int, relative : bool) -> bytes:
        header = CmdHeader(CMD_START_SIGN, CMD_OPCODE_MOUSE_MOVE)
        cur_x, cur_y = GetCursorPos()

        if relative:
            x += cur_x
            y += cur_y

        diff_x, diff_y = cur_x - x, cur_y - y
        move_data = bytes()

        count_x = abs(diff_x // self.MOVE_STEP)
        remainder_x = abs(diff_x % self.MOVE_STEP)
        count_y = abs(diff_y // self.MOVE_STEP)
        remainder_y = abs(diff_y % self.MOVE_STEP)
        move_data = bytes()
        
        sign = 1 if diff_x < 0 else -1
        for _ in range(count_x):
            data = MouseMoveData(sign * self.MOVE_STEP, 0)
            move_data += bytes(header) + bytes(data)

        data = MouseMoveData(sign * remainder_x, 0)
        move_data += bytes(header) + bytes(data)

        sign = 1 if diff_y < 0 else -1
        for _ in range(count_y):
            data = MouseMoveData(0, sign * self.MOVE_STEP)
            move_data += bytes(header) + bytes(data)

        data = MouseMoveData(0, sign * remainder_y)
        move_data += bytes(header) + bytes(data)

        return move_data


    def move(self, x : int , y : int, relative : bool):
        data = self.make_move_data(x, y, relative)
        self.serial.write(data)

    def btn(self, button_code : int , button_status : int):
        header = CmdHeader(CMD_START_SIGN, CMD_OPCODE_MOUSE_BUTTON)
        data = MouseButtonData(button_code, button_status)

        self.serial.write(bytes(header) + bytes(data))