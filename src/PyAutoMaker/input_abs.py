from abc import ABCMeta, abstractmethod

class AbsInput(metaclass = ABCMeta):
    @abstractmethod
    def key(self, key_code : int, key_status : int):
        pass

    @abstractmethod
    def move(self, mode : int, x : int , y : int):
        pass

    @abstractmethod
    def btn(self, button_code : int , button_status : int):
        pass