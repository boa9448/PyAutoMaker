import time

from win32api import GetCursorPos

import env
import PyAutoMaker as pam

#포트 찾아서 인두이노 펌웨어 자동 업로드
pam.upload(pam.get_port_list()[0], "C:\\Program Files (x86)\\Arduino")

#아두이노와 시리얼 통신 시작
arduino = pam.ArduinoUtil(pam.get_port_list()[0], 115200)

arduino.key(ord('A'), pam.ARDUINO_KEY_PRESS) #A입력
arduino.key(ord('A'), pam.ARDUINO_KEY_RELEASE) #B입력

arduino.string("abcde") #문자열 abcde 입력

arduino.btn(pam.ARDUINO_BUTTON_LEFT, pam.ARDUINO_BUTTON_STATUS_PRESS)  #마우스 왼쪽 누르고 있음
arduino.btn(pam.ARDUINO_BUTTON_LEFT, pam.ARDUINO_BUTTON_STATUS_RELEASE)#마우스 왼쪽 땜

arduino.btn(pam.ARDUINO_BUTTON_LEFT, pam.ARDUINO_BUTTON_STATUS_PRESS)  #마우스 왼쪽 누르고 있음
arduino.move(100, 100, True)
arduino.btn(pam.ARDUINO_BUTTON_LEFT, pam.ARDUINO_BUTTON_STATUS_RELEASE)#마우스 왼쪽 땜
time.sleep(3)

print("pre : ", GetCursorPos())
arduino.move(100, 100, True) #현재 좌표에서 100, 100만큼 이동
time.sleep(1)
print("now : ", GetCursorPos())
print("=" * 50)

print("pre : ", GetCursorPos())
arduino.move(100, 100, False) #절대 좌표 100, 100으로 이동
time.sleep(1)
print("now (100, 100): ", GetCursorPos())

del arduino