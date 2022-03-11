class PyAutoMakerBaseException(Exception):
    pass


class HandleException(PyAutoMakerBaseException):
    pass


class ArduinoBaseException(PyAutoMakerBaseException):
    pass


class ArduinoVersionException(ArduinoBaseException):
    pass