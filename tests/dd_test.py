import env
from PyAutoMaker import class_dd

print(class_dd.KEY_LEFT_CTRL)

dd = class_dd.DDUtil()
dd.move(0, 0, False)
dd.key(ord('A'))
dd.key(class_dd.KEY_LEFT_CTRL)