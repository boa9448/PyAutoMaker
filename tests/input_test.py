import time

import env
import PyAutoMaker as pam

port_name = pam.get_port_list()[0]
pam.upload(port_name, "D:\\Program Files (x86)\\Arduino")

# 업로드 후엔 다시 포트 찾아야함
port_name = pam.get_port_list()[0]
input_ = pam.InputUtil(pam.ArduinoUtil, (port_name, 115200))
input_.btn(pam.BUTTON_LEFT, pam.BUTTON_STATUS_PRESS)
input_.btn(pam.BUTTON_LEFT, pam.BUTTON_STATUS_RELEASE)