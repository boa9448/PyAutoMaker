from ctypes import c_byte, c_ubyte, Structure, c_uint16

from input_abs import *

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

CMD_START_SIGN = c_ubyte(ord('#'))
CMD_OPCODE_KEY_DATA = 1
CMD_OPCODE_MOUSE_BUTTON = 2
CMD_OPCODE_MOUSE_MOVE = 3

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