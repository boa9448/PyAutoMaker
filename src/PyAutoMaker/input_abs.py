from abc import ABCMeta, abstractmethod

import win32con

KEY_STATUS_PRESS = 1
KEY_STATUS_RELEASE = 2

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

class AbsInput(metaclass = ABCMeta):
    @abstractmethod
    def key(self, key_code : int, key_status : int):
        pass

    def key_press(self, key_code : int):
        self.key(key_code, KEY_STATUS_PRESS)

    def key_release(self, key_code : int):
        self.key(key_code, KEY_STATUS_RELEASE)

    @abstractmethod
    def move(self, x : int, y : int, relative : bool):
        pass

    @abstractmethod
    def btn(self, button_code : int, button_status : int):
        pass