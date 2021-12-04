from ctypes import c_byte, c_ubyte, Structure, c_uint16

import win32con

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

KEY_PRESS = 1
KEY_RELEASE = 2

BUTTON_LEFT = 1
BUTTON_RIGHT = 2
BUTTON_MIDDLE = 4

BUTTON_STATUS_PRESS = 1
BUTTON_STATUS_RELEASE = 2

KEY_LEFT_CTRL = win32con.VK_LCONTROL
KEY_LEFT_SHIFT = win32con.VK_LSHIFT
KEY_LEFT_ALT = win32con.VK_LMENU
KEY_LEFT_GUI = win32con.VK_LWIN
KEY_RIGHT_CTRL = win32con.VK_RCONTROL
KEY_RIGHT_SHIFT = win32con.VK_RSHIFT
KEY_RIGHT_ALT = win32con.VK_RMENU
KEY_RIGHT_GUI = win32con.VK_RWIN
KEY_UP_ARROW = win32con.VK_UP
KEY_DOWN_ARROW = win32con.VK_DOWN
KEY_LEFT_ARROW = win32con.VK_LEFT
KEY_RIGHT_ARROW = win32con.VK_RIGHT
KEY_BACKSPACE = win32con.VK_BACK
KEY_TAB = win32con.VK_TAB
KEY_RETURN = win32con.VK_RETURN
KEY_ESC = win32con.VK_ESCAPE
KEY_INSERT = win32con.VK_INSERT
KEY_DELETE = win32con.VK_DELETE
KEY_PAGE_UP = win32con.VK_PRIOR
KEY_PAGE_DOWN = win32con.VK_NEXT
KEY_HOME = win32con.VK_HOME
KEY_END = win32con.VK_END
KEY_CAPS_LOCK = win32con.VK_CAPITAL
KEY_F1 = win32con.VK_F1
KEY_F2 = win32con.VK_F2
KEY_F3 = win32con.VK_F3
KEY_F4 = win32con.VK_F4
KEY_F5 = win32con.VK_F5
KEY_F6 = win32con.VK_F6
KEY_F7 = win32con.VK_F7
KEY_F8 = win32con.VK_F8
KEY_F9 = win32con.VK_F9
KEY_F10 = win32con.VK_F10
KEY_F11 = win32con.VK_F11
KEY_F12 = win32con.VK_F12
KEY_F13 = win32con.VK_F13
KEY_F14 = win32con.VK_F14
KEY_F15 = win32con.VK_F15
KEY_F16 = win32con.VK_F16
KEY_F17 = win32con.VK_F17
KEY_F18 = win32con.VK_F18
KEY_F19 = win32con.VK_F19
KEY_F20 = win32con.VK_F20
KEY_F21 = win32con.VK_F21
KEY_F22 = win32con.VK_F22
KEY_F23 = win32con.VK_F23
KEY_F24 = win32con.VK_F24



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