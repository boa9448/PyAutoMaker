import env
import PyAutoMaker as pam

print(pam.KEY_LEFT_CTRL)

dd = pam.DDUtil()
dd.move(0, 0, False)
dd.key(ord('A'))
dd.key(pam.KEY_LEFT_CTRL)