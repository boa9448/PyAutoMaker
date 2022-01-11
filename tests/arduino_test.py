import time
import unittest

from win32api import GetCursorPos

import env
import PyAutoMaker as pam

class TestArduinoModule(unittest.TestCase):
    def __init__(self, methodName: str = ...) -> None:
        super().__init__(methodName=methodName)
        #포트 찾아서 아두이노 펌웨어 자동 업로드
        pam.upload(pam.get_port_list()[0], "C:\\Program Files (x86)\\Arduino")

    def setUp(self) -> None:
        self.arduino = pam.ArduinoUtil(pam.get_port_list()[0], 115200)        
        return super().setUp()