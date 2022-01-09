import random
import time
from queue import Queue

import keyboard
import mouse
import win32api
import win32con

from input_abs import *
from arduino import ArduinoUtil
from class_dd import DDUtil

class InputUtil:
    def __init__(self, backend : ArduinoUtil or DDUtil, args : tuple) -> None:
        self.backend = backend(*args)

    def key(self, key_code : int, key_status : int) -> None:
        return self.backend.key(key_code, key_status)

    def key_press(self, key_code : int) -> None:
        return self.backend.key_press(key_code)

    def key_release(self, key_code : int) -> None:
        return self.backend.key_release(key_code)

    def move(self, x : int , y : int, relative : bool) -> None:
        return self.backend.move(x, y, relative)

    def btn(self, button_code : int , button_status : int) -> None:
        return self.backend.btn(button_code, button_status)

class KeyboardEventEx(keyboard.KeyboardEvent):
    MAPVK_VSC_TO_VK = 1
    MAPVK_VSC_TO_VK_EX = 3
    NUMPAD_MAP = {win32con.VK_DELETE : win32con.VK_DECIMAL
                , win32con.VK_INSERT : win32con.VK_NUMPAD0
                , win32con.VK_END : win32con.VK_NUMPAD1
                , win32con.VK_DOWN : win32con.VK_NUMPAD2
                , win32con.VK_NEXT : win32con.VK_NUMPAD3
                , win32con.VK_LEFT : win32con.VK_NUMPAD4
                , win32con.VK_CLEAR : win32con.VK_NUMPAD5
                , win32con.VK_RIGHT : win32con.VK_NUMPAD6
                , win32con.VK_HOME : win32con.VK_NUMPAD7
                , win32con.VK_UP : win32con.VK_NUMPAD8
                , win32con.VK_PRIOR : win32con.VK_NUMPAD9}

    def __init__(self, event_type, scan_code, name=None, time=None, device=None, modifiers=None, is_keypad=None):
        super().__init__(event_type, scan_code, name=name, time=time, device=device, modifiers=modifiers, is_keypad=is_keypad)
        self.vk_code : int = win32api.MapVirtualKey(scan_code, self.MAPVK_VSC_TO_VK_EX)
        if is_keypad:
            self.vk_code = self.NUMPAD_MAP.get(self.vk_code, self.vk_code)

class Recorder:
    def __init__(self, backend : InputUtil = None) -> None:
        self.backend = backend
        self.mouse_events = None

    def __del__(self) -> None:
        pass

    def key_record_start(self) -> None:
        keyboard.start_recording()

    def key_record_stop(self) -> list:
        key_events = keyboard.stop_recording()

        new_key_events = list()
        for key_event in key_events:
            key_event : keyboard.KeyboardEvent = key_event
            new_key_events.append(KeyboardEventEx(key_event.event_type
                                                    , key_event.scan_code
                                                    , key_event.name
                                                    , key_event.time
                                                    , key_event.device
                                                    , key_event.modifiers
                                                    , key_event.is_keypad))

        return new_key_events

    def key_record(self, stop_key : str = "esc") -> list:
        self.key_record_start()
        keyboard.wait(stop_key)
        key_events = self.key_record_stop()

        new_key_events = list()
        for key_event in key_events:
            key_event : keyboard.KeyboardEvent = key_event
            new_key_events.append(KeyboardEventEx(key_event.event_type
                                                    , key_event.scan_code
                                                    , key_event.name
                                                    , key_event.time
                                                    , key_event.device
                                                    , key_event.modifiers
                                                    , key_event.is_keypad))

        return new_key_events

    def mouse_record_start(self) -> None:
        self.mouse_events = Queue()
        mouse.hook(self.mouse_events.put)

    def mouse_record_stop(self) -> list:
        if self.mouse_events is None:
            return list()

        mouse.unhook(self.mouse_events.put)
        return list(self.mouse_events.queue)

    def mouse_record(self, stop_key : str = "esc") -> list:
        self.mouse_record_start()
        keyboard.wait(stop_key)
        return self.mouse_record_stop()

    def record(self, stop_key : str = "esc") -> list:
        self.key_record_start()
        self.mouse_record_start()
        keyboard.wait(stop_key)
        mouse_events = self.mouse_record_stop()
        key_events = self.key_record_stop()

        events = sorted(key_events + mouse_events, key = lambda x : x.time)
        return events

    def play(self, events : list, rand_delay_range : tuple = (0.03, 0.05)) -> None:

        last_time = None
        for event in events:
            if last_time is not None:
                rand_delay = random.uniform(*rand_delay_range)
                time.sleep(event.time - last_time + rand_delay)

            last_time = event.time
            if isinstance(event, KeyboardEventEx):
                if event.event_type == keyboard.KEY_DOWN:
                    self.backend.key_press(event.vk_code)
                    print(event.vk_code)
                else:
                    self.backend.key_release(event.vk_code)
            else:
                if isinstance(event, mouse.MoveEvent):
                    self.backend.move(event.x, event.y, False)
                elif isinstance(event, mouse.ButtonEvent):
                    if event.event_type == mouse.UP:
                        self.backend.btn(BUTTON_LEFT if mouse.LEFT else BUTTON_RIGHT, BUTTON_STATUS_RELEASE)
                    elif event.event_type == mouse.DOWN:
                        self.backend.btn(BUTTON_LEFT if mouse.LEFT else BUTTON_RIGHT, BUTTON_STATUS_PRESS)
        

if __name__ == "__main__":
    pass
