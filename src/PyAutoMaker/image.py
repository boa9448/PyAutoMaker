import os
from ctypes import wintypes
from ctypes import *

import numpy as np
import cv2

import win32api
import win32con
import win32gui
import win32ui

import utils

class BITMAPINFOHEADER(Structure):
    _fields_ = [
        ('biSize', wintypes.DWORD),
        ('biWidth', wintypes.LONG),
        ('biHeight', wintypes.LONG),
        ('biPlanes', wintypes.WORD),
        ('biBitCount', wintypes.WORD),
        ('biCompression', wintypes.DWORD),
        ('biSizeImage', wintypes.DWORD),
        ('biXPelsPerMeter', wintypes.LONG),
        ('biYPelsPerMeter', wintypes.LONG),
        ('biClrUsed', wintypes.DWORD),
        ('biClrImportant', wintypes.DWORD)
    ]


def screenshotEx(window_name : str = None
                , rect : tuple = None) -> np.ndarray:
    target_window = win32con.NULL

    if window_name:
        target_window = win32gui.FindWindow(win32con.NULL, window_name)
        left, top, right, bottom = rect or win32gui.GetClientRect(target_window)
        width = right - left
        height = bottom - top
    else:
        left, top = 0, 0
        width = win32api.GetSystemMetrics(win32con.SM_CXSCREEN)
        height = win32api.GetSystemMetrics(win32con.SM_CYSCREEN)

    
    targetDC = win32gui.GetDC(target_window)
    compatibleDC = win32gui.CreateCompatibleDC(targetDC)

    win32gui.SetStretchBltMode(compatibleDC, win32con.COLORONCOLOR)

    bitCount = win32ui.GetDeviceCaps(targetDC, win32con.BITSPIXEL)
    img = np.zeros((height, width, 4 if bitCount == 32 else 3), np.uint8)

    bitmap = win32gui.CreateCompatibleBitmap(targetDC, width, height)

    bitmapInfo = BITMAPINFOHEADER()
    bitmapInfo.biSize = sizeof(BITMAPINFOHEADER)
    bitmapInfo.biWidth = width
    bitmapInfo.biHeight = -height
    bitmapInfo.biPlanes = 1
    bitmapInfo.biCompression = win32con.BI_RGB
    bitmapInfo.biSizeImage = 0
    bitmapInfo.biXPelsPerMeter = 0
    bitmapInfo.biYPelsPerMeter = 0
    bitmapInfo.biClrUsed = 0
    bitmapInfo.biClrImportant = 0
    bitmapInfo.biBitCount = bitCount

    win32gui.SelectObject(compatibleDC, bitmap.handle)
    win32gui.BitBlt(compatibleDC, 0, 0, width, height, targetDC, left, top, win32con.SRCCOPY)

    windll.gdi32.GetDIBits(compatibleDC, bitmap.handle, 0, height,
                     cast(img.ctypes.data, POINTER(c_byte)),
                     byref(bitmapInfo),
                     win32con.DIB_RGB_COLORS)

    win32gui.DeleteObject(bitmap)
    win32gui.DeleteDC(compatibleDC)
    win32gui.ReleaseDC(win32con.NULL, targetDC)

    return cv2.cvtColor(img, cv2.COLOR_BGRA2BGR) if img.shape[-1] == 4 else img

class IMAGE(Structure):
    _pack_ = 16
    _fields_ = [("data", POINTER(c_ubyte))
                , ("width", c_int32)
                , ("height", c_int32)
                , ("channels", c_int32)]


class imageUtil:
    def __init__(self):
        dll_path = os.path.join(os.environ["DLL_FOLDER"], "ImageDLL.dll")
        self.dll = windll.LoadLibrary(dll_path)
        self._ImageSearchEx = self.dll["ImageSearchEx"]
        self._ImageSearchEx.argtypes = (wintypes.LPCWSTR, wintypes.LPCWSTR, POINTER(wintypes.RECT), wintypes.DWORD)
        self._ImageSearchEx.restype = wintypes.INT

        self._ImageSearchEx_All = self.dll["ImageSearchEx_All"]
        self._ImageSearchEx_All.argtypes = (wintypes.LPCWSTR, wintypes.LPCWSTR, POINTER(wintypes.RECT), wintypes.UINT, wintypes.DWORD)
        self._ImageSearchEx_All.restype = wintypes.INT

        self._ClearImageMap = self.dll["ClearImageMap"]
        self._ClearImageMap.argtypes = (None, )
        self._ClearImageMap.restype = None

        self._ImageSearchEx_Raw = self.dll["ImageSearchEx_Raw"]
        self._ImageSearchEx_Raw.argtypes = (POINTER(IMAGE), POINTER(IMAGE), POINTER(wintypes.RECT), wintypes.DWORD)
        self._ImageSearchEx_Raw.restype = wintypes.INT

        self._ImageSearchEx_Raw = self.dll["ImageSearchEx_Raw_All"]
        self._ImageSearchEx_Raw.argtypes = (POINTER(IMAGE), POINTER(IMAGE), POINTER(wintypes.RECT), wintypes.UINT, wintypes.DWORD)
        self._ImageSearchEx_Raw.restype = wintypes.INT

        self.find_rects_len = 100
        self.find_rects = (wintypes.RECT * self.find_rects_len)()

    def __del__(self):

        FreeLibrary = windll.kernel32["FreeLibrary"]
        FreeLibrary.argtypes = (wintypes.HMODULE,)
        FreeLibrary.restype = c_int32
        FreeLibrary(self.dll._handle)

    def imageSearchEx(self, src : np.ndarray, temp : np.ndarray, except_color : tuple = (255, 0, 0), find_all : bool = True) -> list:
        src_data = IMAGE(src.ctypes.data_as(POINTER(c_ubyte)), *src.shape)
        temp_data = IMAGE(temp.ctypes.data_as(POINTER(c_ubyte)), *temp.shape)

        if find_all:
            ret = self._ImageSearchEx_All(byref(src_data), byref(temp_data)
                                        , cast(self.find_rects, POINTER(wintypes.RECT)), self.find_rects_len, win32api.RGB(*except_color))
            
            self.find_rects = self.find_rects
            result = [(self.find_rects[idx].left, self.find_rects[idx].top
                        , self.find_rects[idx].right, self.find_rects[idx].bottom) for idx in range(ret)]
        else:
            find_rect = wintypes.RECT()
            ret = self._ImageSearchEx(byref(src_data), byref(temp_data), byref(find_rect), win32api.RGB(*except_color))

            result = [find_rect.left, find_rect.top, find_rect.right, find_rect.bottom]

        return result

searcher = imageUtil()

def imageSearchEx(src : np.ndarray, temp : np.ndarray, except_color : tuple = (255, 0, 0), find_all : bool = True) -> list:
    return searcher.imageSearchEx(src, temp, except_color, find_all)


def cv2_imread(img_path : str, flag : int) -> np.ndarray:
    try:
        data = np.fromfile(img_path, np.uint8)
        img = cv2.imdecode(data, flag)
        img = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR) if img.shape[-1] == 4 else img

        return img
    except Exception as e:
        return None

def cv2_imreads(img_folder_path : str, flag : int = cv2.IMREAD_UNCHANGED) -> dict:
    img_paths = utils.get_image_file_list(os.path.join(img_folder_path, "**", "*.*"))

    img_dict = dict()
    for img_path in img_paths:
        name = img_path.split(os.path.sep)[-1]
        img = cv2_imread(img_path, flag)
        if img is not None:
            img_dict[name] = img

    return img_dict


def template_match(src : np.ndarray, temp : np.ndarray
                , thresh : float = 1.0, except_color : tuple or None = None) -> list:
    """
    src : 3채널 대상이 되는 이미지
    temp : 3채널 찾을 이미지
    thresh : 일치율(임계값)
    except_color : 예외 색상
    """
    
    mask = ...
    if except_color:
        mask = cv2.inRange(temp, except_color, except_color)
        mask = cv2.bitwise_not(mask)
        mask = cv2.cvtColor(mask,cv2.COLOR_GRAY2BGR)
        mask = cv2.bitwise_and(temp.copy(), mask)

    
    result = cv2.matchTemplate(src, temp, cv2.TM_CCORR_NORMED, mask = mask)
    loc = np.where(result >= thresh)

    h, w, c = temp.shape
    rects = [(left, top, left + w, top + h) for left, top in zip(*loc[::-1])]

    return rects

def template_matchs(src : np.ndarray, temps : list
                , thresh : float or list = 1.0, except_color : tuple or None = None):
    """
    src : 3채널 대상이 되는 이미지
    temps : 3채널 찾을 이미지 리스트
    thresh : 일치율(임계값) 또는 각 temp 이미지별 일치율 리스트
    except_color : 예외 색상

    리턴값 : 각 temp이미지별 찾은 위치의 리스트
    list[list[tuple[int, int, int, int]]]
    """
    

    if type(thresh) == float:
        thresh = [thresh for idx in range(len(temps))]

    results = [template_match(src, temp, t, except_color) for temp, t in zip(temps, thresh)]

    return results


if __name__ == "__main__":
    pass
