import time
from typing import Any
import unittest

import win32api

import env
import PyAutoMaker as pam

class TestArduinoModule(unittest.TestCase):
    def __init__(self, methodName: str = ...) -> None:
        super().__init__(methodName=methodName)

    @classmethod
    def setUpClass(cls) -> None:
        pam.arduino.upload()
        return super().setUpClass()

    def setUp(self) -> None:
        self.arduino = pam.arduino.ArduinoUtil(pam.arduino.user_select_port(), 115200)
        return super().setUp()

    def test_key(self) -> None:
        self.arduino.key_press(ord("A"))
        self.arduino.key_release(ord("A"))

    def test_move(self) -> None:
        self.arduino.move(100, 100, False)
        time.sleep(1)
        cur_pos = win32api.GetCursorPos()
        self.assertEqual(cur_pos, (100 ,100))


if __name__ == "__main__":
    unittest.main()