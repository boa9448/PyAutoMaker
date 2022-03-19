import time
import unittest

import win32api

import env
import PyAutoMaker as pam

class TestInputModule(unittest.TestCase):
    def __init__(self, methodName: str = ...) -> None:
        super().__init__(methodName=methodName)

    def test_input_arduino(self) -> None:
        #pam.arduino.upload()
        input_ = pam.input.InputUtil(pam.input.ArduinoUtil, (pam.arduino.user_select_port(), 115200))
        input_.key_press(ord("A"))
        input_.key_release(ord("A"))
        time.sleep(1)

        input_.move(100, 100, False)
        time.sleep(1)
        cur_pos = win32api.GetCursorPos()
        self.assertEqual(cur_pos, (100 ,100))

    def test_input_dd(self) -> None:
        input_ = pam.input.InputUtil(pam.input.DDUtil, tuple())
        input_.key_press(ord("A"))
        input_.key_release(ord("A"))
        time.sleep(1)

        input_.move(100, 100, False)
        time.sleep(1)
        cur_pos = win32api.GetCursorPos()
        self.assertEqual(cur_pos, (100 ,100))

if __name__ == "__main__":
    unittest.main()