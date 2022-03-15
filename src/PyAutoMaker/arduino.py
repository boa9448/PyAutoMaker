import os
import time
from ctypes import c_byte, c_ubyte, Structure, Union, sizeof


from win32api import GetCursorPos
from serial import Serial
from serial.tools import list_ports


from exception import ArduinoBaseException, ArduinoVersionException
from utils import user_select_dir
from input_base import *


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


class FirmwareInfoData(Structure):
    _pack_ = 1
    _fields_ = [("major", c_byte)
                , ("minor", c_byte)
                , ("patch", c_byte)]


class ArduinoData(Union):
    _fields_ = [("key_data", KeyData)
                , ("mouse_button_data", MouseButtonData)
                , ("mouse_move_data", MouseMoveData)
                , ("firmware_info_data", FirmwareInfoData)]


class ArduinoPacket(Structure):
    _pack_ = 1
    _fields_ = [("opcode", c_ubyte)
                , ("data", ArduinoData)]

    def get_version(self) -> FirmwareInfoData:
        if self.opcode != OPCODE_FIRMWARE_INFO_DATA:
            raise ArduinoBaseException("잘못된 응답코드")

        return self.data.firmware_info_data

    def version(self) -> None:
        self.opcode = OPCODE_FIRMWARE_INFO_DATA

    def key(self, key_code : int, key_status : int) -> None:
        self.opcode = OPCODE_KEY_DATA
        self.data.key_data.key_code = key_code
        self.data.key_data.key_status = key_status

    def btn(self, button_code : int, button_status : int) ->None:
        self.opcode = OPCODE_MOUSE_BUTTON_DATA
        self.data.mouse_button_data.button_code = button_code
        self.data.mouse_button_data.button_status = button_status

    def move(self, x : int, y : int) -> None:
        self.opcode = OPCODE_MOUSE_MOVE_DATA
        self.data.mouse_move_data.x = x
        self.data.mouse_move_data.y = y


VERSION_MAJOR = 0
VERSION_MINOR = 1
VERSION_PATCH = 0
FIRMWARE_VERSION = (VERSION_MAJOR, VERSION_MINOR, VERSION_PATCH)

OPCODE_FIRMWARE_INFO_DATA = 1
OPCODE_KEY_DATA = 2
OPCODE_MOUSE_BUTTON_DATA = 3
OPCODE_MOUSE_MOVE_DATA = 4

ARDUINO_KEY_PRESS = 1
ARDUINO_KEY_RELEASE = 2

ARDUINO_BUTTON_LEFT = 1
ARDUINO_BUTTON_RIGHT = 2
ARDUINO_BUTTON_MIDDLE = 4

ARDUINO_BUTTON_STATUS_PRESS = 1
ARDUINO_BUTTON_STATUS_RELEASE = 2


arduino_key_map = {KEY_LEFT_CTRL : 0x80
                    , KEY_LEFT_SHIFT : 0x81
                    , KEY_LEFT_ALT : 0x82
                    , KEY_LEFT_GUI : 0x83
                    , KEY_RIGHT_CTRL : 0x84
                    , KEY_RIGHT_SHIFT : 0x85
                    , KEY_RIGHT_ALT : 0x86
                    , KEY_RIGHT_GUI : 0x87
                    , KEY_UP_ARROW : 0xDA
                    , KEY_DOWN_ARROW : 0xD9
                    , KEY_LEFT_ARROW : 0xD8
                    , KEY_RIGHT_ARROW : 0xD7
                    , KEY_BACKSPACE : 0xB2
                    , KEY_TAB : 0xB3
                    , KEY_RETURN   : 0xB0
                    , KEY_ESC : 0xB1
                    , KEY_INSERT   : 0xD1
                    , KEY_DELETE   : 0xD4
                    , KEY_PAGE_UP  : 0xD3
                    , KEY_PAGE_DOWN : 0xD6
                    , KEY_HOME   : 0xD2
                    , KEY_END : 0xD5
                    , KEY_CAPS_LOCK : 0xC1
                    , KEY_F1 : 0xC2
                    , KEY_F2 : 0xC3
                    , KEY_F3 : 0xC4
                    , KEY_F4 : 0xC5
                    , KEY_F5 : 0xC6
                    , KEY_F6 : 0xC7
                    , KEY_F7 : 0xC8
                    , KEY_F8 : 0xC9
                    , KEY_F9 : 0xCA
                    , KEY_F10 : 0xCB
                    , KEY_F11 : 0xCC
                    , KEY_F12 : 0xCD
                    , KEY_F13 : 0xF0
                    , KEY_F14 : 0xF1
                    , KEY_F15 : 0xF2
                    , KEY_F16 : 0xF3
                    , KEY_F17 : 0xF4
                    , KEY_F18 : 0xF5
                    , KEY_F19 : 0xF6
                    , KEY_F20 : 0xF7
                    , KEY_F21 : 0xF8
                    , KEY_F22 : 0xF9
                    , KEY_F23 : 0xFA
                    , KEY_F24 : 0xFB}



def user_select_port() -> str:
    from PySide6.QtCore import Qt, Slot
    from PySide6.QtWidgets import (QDialog
                                , QApplication
                                , QListWidget
                                , QListWidgetItem
                                , QPushButton
                                , QVBoxLayout
                                , QWidget)
    from qt_material import apply_stylesheet
    
    if QApplication.instance():
        app = QApplication.instance()
    else:
        app = QApplication()

    class PortSelectDialog(QDialog):
        def __init__(self) -> None:
            super().__init__()
            self.setWindowTitle("COM 포트 선택")

            vlayout = QVBoxLayout()
            w = QWidget()
            
            self.port_list = QListWidget()
            self.refresh_button = QPushButton("새로고침")
            
            vlayout.addWidget(self.port_list)
            vlayout.addWidget(self.refresh_button)

            w.setLayout(vlayout)
            self.setLayout(vlayout)

            self.refresh_port_list()
            self.port_list.itemDoubleClicked.connect(self.select_handler)
            self.refresh_button.clicked.connect(self.refresh_button_handler)

            self.selected_port = ""

        def refresh_port_list(self) -> None:
            self.port_list.clear()
            for port in list_ports.comports():
                item = QListWidgetItem()
                item.setText(port.description)
                item.setData(Qt.UserRole, port)
                self.port_list.addItem(item)

        @Slot()
        def refresh_button_handler(self) -> None:
            self.refresh_port_list()

        @Slot()
        def select_handler(self) -> None:
            cur_item = self.port_list.selectedItems()
            if cur_item:
                self.selected_port = cur_item[0].data(Qt.UserRole).device

            self.done(True)

    apply_stylesheet(app, "dark_teal.xml")
    dlg = PortSelectDialog()
    if dlg.exec():
        return dlg.selected_port

    return ""


def upload(port : str = None, arduino_dir : str = "C:\\Program Files (x86)\\Arduino", use_debug : bool = True) -> bool:
    if port is None:
        port = user_select_port()

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


class ArduinoUtil:
    MOVE_STEP = 100

    def __init__(self, port : str, baudrate : int):
        self.serial = Serial(port = port, baudrate = baudrate)
        time.sleep(2)
        self.check_firmware_version()

    def __del__(self):
        if self.serial.is_open:
            self.serial.close()

    def close(self) -> None:
        self.serial.close()

    def get_version(self) -> None:
        data = ArduinoPacket()
        data.version()

        self.serial.write(bytes(data))

    def check_firmware_version(self) -> bool:
        timeout = 3.0
        self.get_version()
        
        data_size = sizeof(ArduinoPacket)
        start_time = time.time()
        while time.time() - start_time < timeout:
            size = self.serial.in_waiting
            if not size:
                time.sleep(0.1)
                continue

            packet : ArduinoPacket = ArduinoPacket.from_buffer_copy(self.serial.read(data_size))
            version_info = packet.get_version()
            if (version_info.major == VERSION_MAJOR
                and version_info.minor == VERSION_MINOR
                and version_info.patch == VERSION_PATCH):

                return

        raise ArduinoVersionException("버전이 일치하지 않거나 잘못된 펌웨어 입니다")

    def key(self, key_code : int, key_status : int) -> bool:
        key_status = ARDUINO_KEY_PRESS if key_status == KEY_STATUS_PRESS else ARDUINO_KEY_RELEASE
        data = ArduinoPacket()
        data.key(key_code, key_status)

        data = bytes(data)
        data_len = len(data)
        return True if self.serial.write(data) == data_len else False

    def key_press(self, key_code : int) -> bool:
        return self.key(key_code, KEY_STATUS_PRESS)

    def key_release(self, key_code : int) -> bool:
        return self.key(key_code, KEY_STATUS_RELEASE)

    def string(self, s : str):
        for c in s:
            self.key_press(ord(c))
            time.sleep(0.03)
            self.key_release(ord(c))
            time.sleep(0.03)

    def btn(self, button_code : int ,button_status : int) -> bool:
        button_status = ARDUINO_BUTTON_STATUS_PRESS if button_status == BUTTON_STATUS_PRESS else ARDUINO_BUTTON_STATUS_RELEASE
        data = ArduinoPacket()
        data.btn(button_code, button_status)

        data = bytes(data)
        data_len = len(data)
        return True if self.serial.write(data) == data_len else False

    def btn_press(self, button_code : int) -> bool:
        return self.btn(button_code, BUTTON_STATUS_PRESS)

    def btn_release(self, button_code : int) -> bool:
        return self.btn(button_code, BUTTON_STATUS_RELEASE)

    def make_move_data(self, x : int , y : int, relative : bool) -> list[ArduinoPacket]:
        cur_x, cur_y = GetCursorPos()

        if relative:
            x += cur_x
            y += cur_y

        diff_x, diff_y = cur_x - x, cur_y - y

        count_x = abs(diff_x // self.MOVE_STEP)
        remainder_x = abs(diff_x % self.MOVE_STEP)
        count_y = abs(diff_y // self.MOVE_STEP)
        remainder_y = abs(diff_y % self.MOVE_STEP)
        move_packet_list = list()
        
        sign = 1 if diff_x < 0 else -1
        for _ in range(count_x):
            data = ArduinoPacket()
            data.move(sign * self.MOVE_STEP, 0)
            move_packet_list.append(data)


        data = ArduinoPacket()
        data.move(sign * remainder_x, 0)
        move_packet_list.append(data)

        sign = 1 if diff_y < 0 else -1
        for _ in range(count_y):
            data = ArduinoPacket()
            data.move(0, sign * self.MOVE_STEP)
            move_packet_list.append(data)

        data = ArduinoPacket()
        data.move(0, sign * remainder_y)
        move_packet_list.append(data)

        return move_packet_list

    def move(self, x : int, y : int) -> bool:
        packet_list = self.make_move_data(x, y, False)
        for packet in packet_list:
            data = bytes(packet)
            data_len = len(data)

            if self.serial.write(data) != data_len:
                return False

        return True

    
if __name__ == "__main__":
    arduino = ArduinoUtil("COM8", 115200)
    arduino.close()
    arduino.key_press(65)
    arduino.key_release(65)