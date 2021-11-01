import os
from ctypes import wintypes, windll

KEY_DOWN = 1 #키다운
KEY_UP = 2 #키업
#btn함수가 사용하는 클릭 코드
MOUSE_LDOWN = 1 #왼쪽 마우스 버튼 다운
MOUSE_LUP = 2 #왼쪽 마우스 버튼 업
MOUSE_RDOWN = 4 #오른쪽 다운
MOUSE_RUP = 8 #오른쪽 업

class DD:
    #key, keyEx함수가 사용하는 키 상태 코드
    KEY_DOWN = KEY_DOWN #키다운
    KEY_UP = KEY_UP #키업
    #btn함수가 사용하는 클릭 코드
    MOUSE_LDOWN = MOUSE_LDOWN #왼쪽 마우스 버튼 다운
    MOUSE_LUP = MOUSE_LUP #왼쪽 마우스 버튼 업
    MOUSE_RDOWN = MOUSE_RDOWN #오른쪽 다운
    MOUSE_RUP = MOUSE_RUP #오른쪽 업

    #일부 함수들은 인자들을 강제할것
    def __init__(self, strDLLPath = os.environ["DLL_FOLDER"] + os.sep + "DD64.dll"):
        #dd 라이브러리를 불러옴
        self.hModule = windll.LoadLibrary(strDLLPath)
        self.DD_key = self.hModule["DD_key"] #DD_key(DD키코드, 키상태)
        self.DD_btn = self.hModule["DD_btn"] #DD_btn(DD클릭 코드)
        self.DD_mov = self.hModule["DD_mov"] #DD_mov(x, y) *** 다중 모니터에선 dd자체 버그가 일어남 ***
        self.DD_movR = self.hModule["DD_movR"] #DD_movR(상대 x, 상대 y) 지금 마우스의 위치에서 상대적으로 움직임
        self.DD_whl = self.hModule["DD_whl"] #마우스 휠인데 지원 안함
        self.DD_todc = self.hModule["DD_todc"] #ddCode = DD_todc(가상키코드) 가상키코드 -> DD코드로 변경
        self.DD_str = self.hModule["DD_str"] #DD_str(입력할 문자열) 문자열은 영어 숫자로만 입력, 대부분의 경우 사용x

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
        FreeLibrary(self.hModule._handle)

    def DD_keyEx(self, vkeyCode, keyState):
        #todc함수는 가상키 코드를 드라이버에서 사용하는 코드로 변환함
        #가상 키코드 -> dd코드로 변환
        #DD_key함수 호출
        self.DD_key(self.DD_todc(vkeyCode), keyState)