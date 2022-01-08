PyAutoMaker
========
자동화를 위한 파이썬 패키지  
개발중인 버전이며 내보낸 API는 언제든지 변경될 수 있습니다  



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
스크린샷을 찍는 방법  


```
import cv2

import PyAutoMaker as pam

img = pam.screenshotEx()
cv2.imshow("screenshot", img)
cv2.waitKey()
cv2.destroyAllWindows()
```  

특정 이름을 가진 창의 스크린샷을 찍는 방법
```
import cv2

import PyAutoMaker as pam

img = pam.screenshotEx("MapleStory")
cv2.imshow("screenshot", img)
cv2.waitKey()
cv2.destroyAllWindows()
```

화면에서 이미지서치를 사용하는 방법  

```
import cv2

import PyAutoMaker as pam

src = pam.screenshotEx()
temp = cv2.imread("temp.png")
result = pam.imageSearchEx(src, temp)

for left, top, right, bottom in result:
    cv2.rectangle(src, (left, top), (right, bottom), (0, 255, 0), 2)

cv2.imshow("view", src)
cv2.waitKey()
cv2.destroyAllWindows()
```
