from ctypes import POINTER, Structure, c_byte, c_short, c_ushort

class KeyData(Structure):
    _pack_ = 1
    _fields_ = [("key_code", c_byte)
                , ("key_status", c_byte)]


class MouseButtonData(Structure):
    _pack_ = 1
    _fields_ = [("button_code", c_byte)
                , ("button_status", c_byte)]


class MouseMoveData(Structure):
    _pack_ = 1
    _fields_ = [("move_type", c_byte)
                ,("move_mode", c_byte)
                , ("x", c_short)
                , ("y", c_short)]


class InputPacket(Structure):
    _pack_ = 1
    _fields_ = [("start_sign", c_byte)
                , ("data_type", c_byte)
                , ("data_size", c_ushort)
                , ("data_pointer", POINTER(c_byte))
                , ("end_sign", c_byte)]