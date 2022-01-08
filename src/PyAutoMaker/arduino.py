import os
import time
from threading import Thread, Event

from win32api import GetCursorPos
from serial import Serial
from serial.tools import list_ports

from input_abs import *
from arduino_define import *
from utils import user_select_dir

def get_port_list(name : str or list = ["USB 직렬 장치", "Leonardo"]) -> list:
    find_port_list = list_ports.comports()
    port_list = list()
    if type(name) == str:
        name_list = [name]
    else:
        name_list = name

    for port in find_port_list:
        port_list = [port.device for name in name_list if name in port.description]

    return port_list

def upload(port : str, arduino_dir : str = "C:\\Program Files (x86)\\Arduino", use_debug : bool = True) -> bool:
    arduino_bin = "arduino_debug.exe" if use_debug else "arduino.exe"
    arduino_bin_full_path = os.path.join(arduino_dir, arduino_bin)
    if not os.path.isfile(arduino_bin_full_path):
        arduino_dir = user_select_dir()
        arduino_bin_full_path = os.path.join(arduino_dir, arduino_bin)

    cur_dir = os.path.dirname(__file__)
    src_path = os.path.abspath(os.path.join(cur_dir, "arduino_keyboard_src", "arduino_keyboard_src.ino"))
    upload_command = f"\"{arduino_bin_full_path}\" --board arduino:avr:leonardo --port {port} --upload {src_path}"

    ret_code = os.system(upload_command)
    return True if ret_code == 0 else False

class DebugThread(Thread):
    def __init__(self, serial : Serial):
        super().__init__()
        self.exit_event = Event()
        self.serial = serial

    def __del__(self):
        pass

    def run(self) -> None:
        while self.exit_event.is_set() == False:
            if self.serial.inWaiting() > 0:
                data = self.serial.read(self.serial.in_waiting)
                data = data.decode("ascii")
                print(data)

    def exit(self) -> None:
        self.exit_event.set()

    def join(self) -> bool:
        self.exit()
        return super().join()

class ArduinoUtil(AbsInput):
    MOVE_STEP = 100

    def __init__(self, port : str, baudrate : int):
        self.serial = Serial(port = port, baudrate = baudrate)
        time.sleep(2)

    def __del__(self):
        self.serial.close()

    def key(self, key_code : int, key_status : int) -> int:
        header = CmdHeader(CMD_START_SIGN, CMD_OPCODE_KEY_DATA)
        data = KeyData(arduino_key_map.get(key_code, key_code), key_status)

        data = bytes(header) + bytes(data)
        return self.serial.write(data)

    def key_press(self, key_code : int) -> None:
        self.key(key_code, ARDUINO_KEY_PRESS)

    def key_release(self, key_code : int):
        self.key(key_code, ARDUINO_KEY_RELEASE)

    def string(self, s : str):
        for c in s:
            self.key_press(ord(c))
            self.key_release(ord(c))
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


    def move(self, x : int, y : int, relative : bool):
        data = self.make_move_data(x, y, relative)
        self.serial.write(data)

    def btn(self, button_code : int, button_status : int):
        header = CmdHeader(CMD_START_SIGN, CMD_OPCODE_MOUSE_BUTTON)
        data = MouseButtonData(button_code, button_status)

        self.serial.write(bytes(header) + bytes(data))