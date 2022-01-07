import numpy as np
import cv2
import time
import win32api
import win32con
import win32gui
import win32ui
import os
import sys
from ctypes import wintypes
from ctypes import windll
from ctypes import *

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


def screenshotEx(window_name = None, start = (0, 0), end = (0, 0)):
    target_window = win32con.NULL
    if window_name:
        target_window = win32gui.FindWindow(win32con.NULL, window_name)
        
    if target_window == win32con.NULL:
        width = end[0] - start[0]
        height = end[1] - start[1]

        if width == 0 and height == 0:
            width = win32api.GetSystemMetrics(win32con.SM_CXSCREEN)
            height = win32api.GetSystemMetrics(win32con.SM_CYSCREEN)
    else:
        width = end[0] - start[0]
        height = end[1] - start[1]

        if width == 0 and height == 0:
            wndRect = win32gui.GetClientRect(target_window)
            width = wndRect[2] - wndRect[0]
            height = wndRect[3] - wndRect[1]

        
    
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
    win32gui.BitBlt(compatibleDC, 0, 0, width, height, targetDC, *start, win32con.SRCCOPY)

    windll.gdi32.GetDIBits(compatibleDC, bitmap.handle, 0, height,
                     cast(img.ctypes.data, POINTER(c_byte)),
                     byref(bitmapInfo),
                     win32con.DIB_RGB_COLORS)

    win32gui.DeleteObject(bitmap)
    win32gui.DeleteDC(compatibleDC)
    win32gui.ReleaseDC(win32con.NULL, targetDC)

    return cv2.cvtColor(img, cv2.COLOR_BGRA2BGR) if img.shape[-1] == 4 else img

class IMAGE_DATA(Structure):
    _fields_ = [("lpData", c_ulonglong)
                , ("nHeight", c_uint)
                , ("nWidth", c_uint)
                , ("nChannel", c_uint)]


class imageUtil:
    def __init__(self):
        self.dll = windll.LoadLibrary(os.environ["DLL_FOLDER"] + os.sep + "PythonWrapper.dll")
        self.__ImageSearchEx = self.dll["ImageSearchEx"]
        self.__ImageSearchEx.argtypes = (POINTER(IMAGE_DATA), POINTER(IMAGE_DATA), POINTER(wintypes.RECT), c_ulong)
        self.__ImageSearchEx.restype = (c_int)

        self.__ImageSearchExAll = self.dll["ImageSearchExAll"]
        self.__ImageSearchExAll.argtypes = (POINTER(IMAGE_DATA), POINTER(IMAGE_DATA), POINTER(wintypes.RECT), c_uint, c_ulong)
        self.__ImageSearchExAll.restype = (c_int)

        self.__imageSearchEx_Parallel = self.dll["ImageSearchEx_Parallel"]
        self.__imageSearchEx_Parallel.argtypes = (POINTER(IMAGE_DATA), POINTER(IMAGE_DATA), POINTER(wintypes.RECT), c_ulong)
        self.__imageSearchEx_Parallel.restype = (c_int)
        
        self.__imageSearchExAll_Parallel = self.dll["ImageSearchExAll_Parallel"]
        self.__imageSearchExAll_Parallel.argtypes = (POINTER(IMAGE_DATA), POINTER(IMAGE_DATA), POINTER(wintypes.RECT), c_uint, c_ulong)
        self.__imageSearchExAll_Parallel.restype = (c_int)

        self.__imageSearchEx_Parallel_ = self.dll["ImageSearchEx_Parallel_"]
        self.__imageSearchEx_Parallel_.argtypes = (POINTER(IMAGE_DATA), POINTER(IMAGE_DATA), POINTER(wintypes.RECT), c_float, c_ulong)
        self.__imageSearchEx_Parallel_.restype = (c_int)
        
        self.__imageSearchExAll_Parallel_ = self.dll["ImageSearchExAll_Parallel_"]
        self.__imageSearchExAll_Parallel_.argtypes = (POINTER(IMAGE_DATA), POINTER(IMAGE_DATA), POINTER(wintypes.RECT), c_uint, c_float, c_ulong)
        self.__imageSearchExAll_Parallel_.restype = (c_int)

    def __del__(self):
        FreeLibrary = windll.kernel32["FreeLibrary"]
        FreeLibrary.argtypes = (wintypes.HMODULE,)
        FreeLibrary.restype = (c_int)
        FreeLibrary(self.dll._handle)

    def imageSearchEx(self, src, temp, exceptColor = (255, 0, 0), findAll = True):
        src = cv2.cvtColor(src, cv2.COLOR_BGRA2BGR) if src.shape[-1] == 4 else src
        temp = cv2.cvtColor(temp, cv2.COLOR_BGRA2BGR) if temp.shape[-1] == 4 else temp


        src_data = IMAGE_DATA(src.ctypes.data, *src.shape)
        temp_data = IMAGE_DATA(temp.ctypes.data, *temp.shape)

        if findAll:
            resultLen = 100
            result = (wintypes.RECT * resultLen)()

            ret = self.__ImageSearchExAll(byref(src_data), byref(temp_data), cast(result, POINTER(wintypes.RECT)), resultLen, exceptColor)
            if ret <= 0:
                return []

            result = [(result[idx].left, result[idx].top, result[idx].right, result[idx].bottom) for idx in range(ret)]

        else:
            result = wintypes.RECT()
            ret = self.__ImageSearchEx(byref(src_data), byref(temp_data), byref(result), exceptColor)
            if ret <= 0:
                return []

            result = [result.left, result.top, result.right, result.bottom]

        return result

    def imageSearchEx_Parallel(self, src, temp, exceptColor = (255, 0, 0), rate = float(0.95)):
        src = cv2.cvtColor(src, cv2.COLOR_BGRA2BGR) if src.shape[-1] == 4 else src
        temp = cv2.cvtColor(temp, cv2.COLOR_BGRA2BGR) if temp.shape[-1] == 4 else temp

        src_data = IMAGE_DATA(src.ctypes.data, *src.shape)
        temp_data = IMAGE_DATA(temp.ctypes.data, *temp.shape)

        resultLen = 100
        result = (wintypes.RECT * resultLen)()
        ret = self.__imageSearchExAll_Parallel_(byref(src_data), byref(temp_data), cast(result, POINTER(wintypes.RECT)), resultLen, rate, exceptColor)
        result = [(result[idx].left, result[idx].top, result[idx].right, result[idx].bottom) for idx in range(ret)]

        return result

searcher = imageUtil()

def imread(strFilePath, flags = cv2.IMREAD_UNCHANGED):
    data = np.fromfile(strFilePath, np.uint8)
    img = cv2.imdecode(data, flags)
    return img

def imageSearchEx(src, temp, exceptColor = (255, 0, 0)):
    return searcher.imageSearchEx(src, temp, win32api.RGB(*exceptColor))

def imageSearchEx_Parallel(src, temp, exceptColor = (255, 0, 0), rate = float(0)):
    return searcher.imageSearchEx_Parallel(src, temp, win32api.RGB(*exceptColor), rate)

def templateMatching(src, temp, thresh):
    size = temp.shape

    res = cv2.matchTemplate(src, temp, cv2.TM_CCOEFF_NORMED)
    loc = np.where( res >= thresh)
    result = []
    for pt in zip(*loc[::-1]):
        #result.append([pt[0], pt[1], pt[0] + w, pt[1] + h])
        result.append([pt[0], pt[1], pt[0] + size[1], pt[1] + size[0]])

    return result

def templateMatchingEx(src, temp, thresh, exceptColor):
    #h, w, _ = temp.shape
    size = temp.shape
    
    upper = exceptColor[::-1]
    lower = upper

    mask = cv2.inRange(temp, lower, upper)
    mask = cv2.bitwise_not(mask)

    res = cv2.matchTemplate(src,temp,cv2.TM_CCOEFF_NORMED, mask = mask)
    loc = np.where( res >= thresh)
    result = []
    for pt in zip(*loc[::-1]):
        #result.append([pt[0], pt[1], pt[0] + w, pt[1] + h])
        result.append([pt[0], pt[1], pt[0] + size[1], pt[1] + size[0]])

    return result


def extractMask(img, lower, upper):
    img = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR) if img.shape[2] == 4 else img

    img_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    img_mask = cv2.inRange(img_hsv, lower, upper)

    return img_mask


if __name__ == "__main__":
    pass
