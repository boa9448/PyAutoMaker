from abc import ABCMeta, abstractmethod

class AbsInput(metaclass = ABCMeta):
    @abstractmethod
    def key(self, key_code : int, key_status : int):
        pass

    @abstractmethod
    def move(self, x : int , y : int, relative : bool):
        pass

    @abstractmethod
    def btn(self, button_code : int , button_status : int):
        pass