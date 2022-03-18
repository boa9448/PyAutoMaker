import unittest
import time

import win32api

import env
import PyAutoMaker as pam

class TestClassDDModule(unittest.TestCase):
    def __init__(self, methodName: str = ...) -> None:
        self.dd = pam.class_dd.DDUtil()
        super().__init__(methodName=methodName)

    def test_key(self) -> None:
        self.dd.key_press(ord("A"))
        self.dd.key_release(ord("A"))

    def test_move(self) -> None:
        self.dd.move(100, 100, False)
        time.sleep(1)
        cur_pos = win32api.GetCursorPos()
        self.assertEqual(cur_pos, (100 ,100))

if __name__ == "__main__":
    unittest.main()