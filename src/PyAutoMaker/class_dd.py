import os
from ctypes import c_char_p, wintypes, windll, c_int32

from input_abs import *

class DDUtil(AbsInput):
    DD_KEY_PRESS = 1 #키다운
    DD_KEY_RELEASE = 2 #키업
    #btn함수가 사용하는 클릭 코드
    DD_MOUSE_LDOWN = 1 #왼쪽 마우스 버튼 다운
    DD_MOUSE_LUP = 2 #왼쪽 마우스 버튼 업
    DD_MOUSE_RDOWN = 4 #오른쪽 다운
    DD_MOUSE_RUP = 8 #오른쪽 업

    def __init__(self, strDLLPath = os.path.join(os.environ["DLL_FOLDER"], "DD64.dll")):
        #dd 라이브러리를 불러옴
        self._hModule = windll.LoadLibrary(strDLLPath)
        self._DD_key = self._hModule["DD_key"] #DD_key(DD키코드, 키상태)
        self._DD_key.argtypes = (c_int32, c_int32)
        self._DD_key.restype = c_int32

        self._DD_btn = self._hModule["DD_btn"] #DD_btn(DD클릭 코드)
        self._DD_btn.argtypes = (c_int32,)
        self._DD_btn.restype = c_int32

        self._DD_mov = self._hModule["DD_mov"] #DD_mov(x, y) *** 다중 모니터에선 dd자체 버그가 일어남 ***
        self._DD_mov.argtypes = (c_int32, c_int32)
        self._DD_mov.restype = c_int32

        self._DD_movR = self._hModule["DD_movR"] #DD_movR(상대 x, 상대 y) 지금 마우스의 위치에서 상대적으로 움직임
        self._DD_movR.argtypes = (c_int32, c_int32)
        self._DD_movR.restype = c_int32

        self._DD_whl = self._hModule["DD_whl"] #마우스 휠
        self._DD_whl.argtypes = (c_int32,)
        self._DD_whl.restype = c_int32

        self._DD_todc = self._hModule["DD_todc"] #ddCode = DD_todc(가상키코드) 가상키코드 -> DD코드로 변경
        self._DD_todc.argtypes = (c_int32,)
        self._DD_todc.restype = c_int32

        self._DD_str = self._hModule["DD_str"] #DD_str(입력할 문자열) 문자열은 영어 숫자로만 입력, 대부분의 경우 사용x
        self._DD_str.argtypes = (c_char_p,)
        self._DD_str.restype = c_int32

    def __del__(self):
        #소멸자 함수
        #windll을 통해서 로드한 dll은 명시적으로 해제할 필요는 없음
        #버그의 여지나 반드시 해제해야하는 라이브러리는 명시적으로 해제
        
        #FreeLibrary함수 객체 생성
        FreeLibrary = windll.kernel32["FreeLibrary"]
        #함수의 인자를 강제함
        FreeLibrary.argtypes = (wintypes.HMODULE,)
        #실제 함수를 호출
        #hModule = dd의 dll객체, hModule._handle = dll의 핸들
        FreeLibrary(self._hModule._handle)

    def btn(self, button_code: int, button_status: int):
        if button_code == BUTTON_LEFT and button_status == BUTTON_STATUS_PRESS:
            self._DD_btn(self.DD_MOUSE_LDOWN)
        elif button_code == BUTTON_LEFT and button_status == BUTTON_STATUS_RELEASE:
            self._DD_btn(self.DD_MOUSE_LUP)
        elif button_code == BUTTON_RIGHT and button_status == BUTTON_STATUS_PRESS:
            self._DD_btn(self.DD_MOUSE_RDOWN)
        elif button_code == BUTTON_RIGHT and button_status == BUTTON_STATUS_RELEASE:
            self._DD_btn(self.DD_MOUSE_RUP)
        elif button_code == BUTTON_MIDDLE and button_status == BUTTON_STATUS_PRESS:
            pass
        elif button_code == BUTTON_MIDDLE and button_status == BUTTON_STATUS_RELEASE:
            pass

    def key(self, key_code : int, key_status : int):
        key_status = self.DD_KEY_PRESS if key_status == KEY_STATUS_PRESS else self.DD_KEY_RELEASE
        self._DD_key(self._DD_todc(key_code), key_status)

    def move(self, x: int, y: int, relative: bool):
        if not relative:
            self._DD_mov(x, y)
        else:
            self._DD_movR(x, y)

if __name__ == "__main__":
    pass

    