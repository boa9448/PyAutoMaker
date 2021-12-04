PyAutoMaker
========
자동화를 위한 파이썬 패키지

개발중인 버전이라 내보낸 API는 언제든지 변경될 수 있습니다


설치방법
========

[PyPI package](https://pypi.python.org/pypi/PyAutoMaker/)에서 설치하는 방법

    pip install PyAutoMaker

또는 저장소에서 클론하는 방법

    git clone https://github.com/boa9448/PyAutoMaker
    cd PyAutoMaker
    python setup.py install


사용방법
========

ClassDD를 이용한 키보드, 마우스 입력

    from PyAutoMaker.dd import DD

    dd = DD()

    #A입력
    dd.DD_keyEx(65, DD.KEY_DOWN)
    dd.DD_keyEx(65, DD.KEY_UP)


    #100, 100좌표로 마우스 이동
    dd.DD_mov(100, 100)

    #마우스 좌클릭
    dd.DD_btn(DD.MOUSE_LDOWN)
    dd.DD_btn(DD.MOUSE_LUP)

    #마우스를 지금 좌표에서 상대적으로 이동
    dd.DD_movR(10, 10)


arduino leonardo를 이용한 키보드, 마우스 입력

        #포트 찾아서 인두이노 펌웨어 자동 업로드
    upload(get_port_list(), "D:\\Program Files (x86)\\Arduino")

    #아두이노와 시리얼 통신 시작
    arduino = ArduinoUtil(get_port_list(), 9600)
    time.sleep(2)

    arduino.key(ord('A')) #A입력
    arduino.key(ord('B')) #B입력

    arduino.string("abcde") #문자열 abcde 입력

    arduino.btn(BUTTON_LEFT, BUTTON_STATUS_PRESS)  #마우스 왼쪽 누르고 있음
    arduino.btn(BUTTON_LEFT, BUTTON_STATUS_RELEASE)#마우스 왼쪽 땜

    arduino.btn(BUTTON_LEFT, BUTTON_STATUS_PRESS)  #마우스 왼쪽 누르고 있음
    arduino.move(100, 100, True)
    arduino.btn(BUTTON_LEFT, BUTTON_STATUS_RELEASE)#마우스 왼쪽 땜
    time.sleep(30)

    print("pre : ", GetCursorPos())
    arduino.move(100, 100, True) #현재 좌표에서 100, 100만큼 이동
    time.sleep(1)
    print("now : ", GetCursorPos())

    print("pre : ", GetCursorPos())
    arduino.move(100, 100, False) #절대 좌표 100, 100으로 이동
    time.sleep(1)
    print("now : ", GetCursorPos())