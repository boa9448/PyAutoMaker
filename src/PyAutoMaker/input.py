from queue import Queue

import keyboard
import mouse
import win32api

from input_abs import *
from arduino import ArduinoUtil
from class_dd import DDUtil

class InputUtil:
    def __init__(self, backend : ArduinoUtil or DDUtil, args : tuple) -> None:
        self.backend = backend(*args)

    def key(self, key_code : int, key_status : int) -> None:
        return self.backend.key(key_code, key_status)

    def move(self, x : int , y : int, relative : bool) -> None:
        return self.backend.move(x, y, relative)

    def btn(self, button_code : int , button_status : int) -> None:
        return self.backend.btn(button_code, button_status)

class KeyboardEventEx(keyboard.KeyboardEvent):
    MAPVK_VSC_TO_VK_EX = 3

    def __init__(self, event_type, scan_code, name=None, time=None, device=None, modifiers=None, is_keypad=None):
        super().__init__(event_type, scan_code, name=name, time=time, device=device, modifiers=modifiers, is_keypad=is_keypad)
        self.vk_code : int = win32api.MapVirtualKey(scan_code, self.MAPVK_VSC_TO_VK_EX)

class Recorder:
    def __init__(self, backend : InputUtil) -> None:
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

    def play(self, events : list, rand_delay_range : tuple = (30, 50)) -> None:
        for event in events:
            if isinstance(event, KeyboardEventEx):
                pass

            else:
                if isinstance(event, mouse.MoveEvent):
                    pass
                elif isinstance(event, mouse.ButtonEvent):
                    pass
        


    

if __name__ == "__main__":
    pass
