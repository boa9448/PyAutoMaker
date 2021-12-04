import os
import time
from ctypes import Structure, c_byte, c_ubyte, c_uint16

from win32api import GetCursorPos
from serial import Serial
from serial.tools import list_ports

from input_abs import AbsInput
from arduino_define import *

class CmdHeader(Structure):
    _pack_ = 1
    _fields_ = [("start_sign", c_ubyte)
                , ("opcode", c_uint16)]

class KeyData(Structure):
    _pack_ = 1
    _fields_ = [("key_code", c_ubyte)
                , ("key_status", c_ubyte)]


class MouseButtonData(Structure):
    _pack_ = 1
    _fields_ = [("button_code", c_ubyte)
                , ("button_status", c_ubyte)]


class MouseMoveData(Structure):
    _pack_ = 1
    _fields_ = [("x", c_byte)
                , ("y", c_byte)]



def get_port_list(name = "USB 직렬 장치") -> str or None:
    port_list = list_ports.comports()
    for port in port_list:
        if name in port.description:
            return port.device

    return None

def upload(port : str) -> bool:
    os.environ["path"] = os.pathsep.join([os.environ["path"], "D:\\Program Files (x86)\\Arduino"])
    cur_dir = os.path.dirname(__file__)
    src_path = os.path.abspath(os.path.join(cur_dir, "arduino_keyboard_src", "arduino_keyboard_src.ino"))
    upload_command = f"arduino_debug.exe --board arduino:avr:leonardo --port {port} --upload {src_path}"

    ret_code = os.system(upload_command)
    return True if ret_code == 0 else False

class ArduinoUtil(AbsInput):
    MOVE_STEP = c_ubyte(-1).value // 2

    def __init__(self, port : str, baudrate : int):
        self.serial = Serial(port = port, baudrate = baudrate)

    def __del__(self):
        self.serial.close()

    def log(func):
        def wrapper(*args, **kwargs):
            func(*args, **kwargs)
            arduino = args[0]
            data = arduino.serial.read_all()
            print(data)

        return wrapper

    @log
    def key(self, key_code : int) -> int:
        write_count = self.key_press(key_code)
        write_count += self.key_release(key_code)

        return write_count

    @log
    def key_press(self, key_code : int) -> int:
        header = CmdHeader(CMD_START_SIGN, CMD_OPCODE_KEY_DATA)
        data = KeyData(arduino_key_map.get(key_code, key_code), KEY_PRESS)

        data = bytes(header) + bytes(data)
        return self.serial.write(data)

    @log
    def key_release(self, key_code : int) -> int:
        header = CmdHeader(CMD_START_SIGN, CMD_OPCODE_KEY_DATA)
        data = KeyData(arduino_key_map.get(key_code, key_code), KEY_RELEASE)

        data = bytes(header) + bytes(data)
        return self.serial.write(data)

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


    @log
    def move(self, x : int , y : int, relative : bool) -> int:
        data = self.make_move_data(x, y, relative)
        return self.serial.write(data)

    @log
    def btn(self, button_code : int , button_status : int) -> int:
        header = CmdHeader(CMD_START_SIGN, CMD_OPCODE_MOUSE_BUTTON)
        data = MouseButtonData(button_code, button_status)

        return self.serial.write(bytes(header) + bytes(data))


if __name__ == "__main__":
    #upload(get_port_list())
    arduino = ArduinoUtil(get_port_list(), 9600)
    time.sleep(2)
    
    arduino.key(65)
    arduino.key(65)
    arduino.btn(BUTTON_LEFT, BUTTON_STATUS_PRESS)
    arduino.btn(BUTTON_LEFT, BUTTON_STATUS_RELEASE)
    arduino.move(100, 100, False)
    print("wait...")
    time.sleep(1)
    data = arduino.serial.read_all()
    print(data)