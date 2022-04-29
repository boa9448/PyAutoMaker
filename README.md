# PyAutoMaker
----  
자동화를 위한 파이썬 패키지  
개발중인 버전이며 내보낸 API는 언제든지 변경될 수 있습니다  



# 설치방법
----  

[PyPI package](https://pypi.python.org/pypi/PyAutoMaker/)에서 설치하는 방법

    pip install PyAutoMaker -U

또는 저장소에서 클론하는 방법

    git clone https://github.com/boa9448/PyAutoMaker
    cd PyAutoMaker
    python setup.py install


# 사용방법
----  

## 특정 이름을 가진 창의 핸들을 구하는 방법  
```
import PyAutoMaker as pam

handle_list : list[int] = pam.utils.get_window_handle("제목 없음 - Windows 메모장")
```

## 데스크탑 스크린샷을 찍는 방법  
```
import cv2

import PyAutoMaker as pam

#화면 스크린샷
img = pam.image.desktop_screenshot()
cv2.imshow("desktop_screenshot", img)
cv2.waitKey()
cv2.destroyAllWindows()
```  

## 특정 이름을 가진 창의 스크린샷을 찍는 방법  
```
import cv2

import PyAutoMaker as pam

#화면 스크린샷
img = pam.image.screenshotEx("MapleStory", rect = (0, 0, 500, 500))
cv2.imshow("screenshotEx", img)
cv2.waitKey()
cv2.destroyAllWindows()
```

## 화면에서 이미지서치를 사용하는 방법  
```
import cv2

import PyAutoMaker as pam

src = pam.image.desktop_screenshot()
temp = cv2.imread("temp.png")
result = pam.imageSearchEx(src, temp)

for left, top, right, bottom in result:
    cv2.rectangle(src, (left, top), (right, bottom), (0, 255, 0), 2)

cv2.imshow("view", src)
cv2.waitKey()
cv2.destroyAllWindows()
```

## 아두이노를 사용해서 키보드 마우스를 입력하는 방법  
```
import PyAutoMaker as pam

#펌웨어는 처음 한번만 업로드 하세요
#pam.arduino.upload()

arduino = pam.arduino.ArduinoUtil(pam.arduino.user_select_port(), 115200)

#A 입력
arduino.key_press(ord("A"))
arduino.key_release(ord("A"))

#컨트롤 키 입력
arduino.key_press(pam.input.KEY_LEFT_CTRL)
arduino.key_release(pam.input.KEY_LEFT_CTRL)

#100, 100좌표로 이동
arduino.move(100, 100, False)

#현재 좌표에서 100, 100만큼 이동
arduino.move(100, 100, True)


#마우스 좌클릭
arduino.btn_press(pam.input.BUTTON_LEFT)
arduino.btn_release(pam.input.BUTTON_LEFT)
```


## class dd를 사용해서 키보드 마우스를 입력하는 방법  
```
import PyAutoMaker as pam

dd = pam.class_dd.DDUtil()

#A 입력
dd.key_press(ord("A"))
dd.key_release(ord("A"))

#100, 100좌표로 이동
dd.move(100, 100, False)

#현재 좌표에서 100, 100만큼 이동
dd.move(100, 100, True)

#마우스 좌클릭
dd.btn_press(pam.input.BUTTON_LEFT)
dd.btn_release(pam.input.BUTTON_LEFT)
```

## 또는...  
```
import PyAutoMaker as pam

#아두이노를 사용할 때는 펌웨어를 처음 한번만 업로드 하세요
#pam.arduino.upload()

#아두이노 사용
input_ = pam.input.InputUtil(pam.input.ArduinoUtil, (pam.arduino.user_select_port(), 115200))

#또는 class dd사용
#input_ = pam.input.InputUtil(pam.input.DDUtil, tuple())

#A 입력
input_.key_press(ord("A"))
input_.key_release(ord("A"))

#컨트롤 키 입력
input_.key_press(pam.input.KEY_LEFT_CTRL)
input_.key_release(pam.input.KEY_LEFT_CTRL)

#100, 100좌표로 이동
input_.move(100, 100, False)

#현재 좌표에서 100, 100만큼 이동
input_.move(100, 100, True)


#마우스 좌클릭
input_.btn_press(pam.input.BUTTON_LEFT)
input_.btn_release(pam.input.BUTTON_LEFT)
```

## opencv dnn darknet을 사용하는 방법  
```
import cv2

import PyAutoMaker as pam


img = pam.image.desktop_screenshot()
detector = pam.darknet.DarknetUtil("your_model.cfg", "your_model.weights", (416, 416))

results = detector.detect(desktop_screenshot, thresh = 0.85)
print(results)
```