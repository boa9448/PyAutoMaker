import sys

import mouse
from PySide6.QtCore import QObject, Qt, Signal, Slot
from PySide6.QtWidgets import QMainWindow, QApplication, QTableWidgetItem
from qt_material import apply_stylesheet
from PyAutoMaker.arduino import get_port_list

from input import InputUtil, Recorder, ArduinoUtil, KeyboardEventEx
from gui_form import input_form


def record_test():
    class RecordSignal(QObject):
        sig = Signal(object)

        def __init__(self):
            super().__init__()

        def insert_event(self, event : object):
            self.sig.emit(event)

    class MainWindow(QMainWindow, input_form.Ui_MainWindow):
        COL_NAME_LIST = ["타입", "파라미터1", "파라미터2", "파라미터3", "파라미터4"]
        COL_NAME_SIZE_LIST = [200, 200, 200, 200, 200]

        def __init__(self):
            super(MainWindow, self).__init__()
            self.setupUi(self)
            self.init_data()
            self.init_handler()
            self.init_display()
        
        def init_data(self) -> None:
            self.input = InputUtil(ArduinoUtil, (get_port_list()[0], 115200))
            self.is_key_recorded = False
            self.is_mouse_recorded = False
            self.recorder = Recorder(self.input)
            self.record_signal = RecordSignal()
            self.record_signal.sig.connect(self.record_signal_handler)

        def init_handler(self) -> None:
            self.key_record_button.clicked.connect(self.key_record_button_handler)
            self.mouse_record_button.clicked.connect(self.mouse_record_button_handler)
            self.key_mouse_record_button.clicked.connect(self.key_mouse_record_button_handler)
            self.save_file_button.clicked.connect(print)
            self.load_file_button.clicked.connect(print)
            self.start_button.clicked.connect(self.start_button_handler)

        def init_display(self) -> None:
            count = len(self.COL_NAME_LIST)
            self.data_table.setColumnCount(count)
            self.data_table.setHorizontalHeaderLabels(self.COL_NAME_LIST)
            for idx, width in enumerate(self.COL_NAME_SIZE_LIST):
                self.data_table.setColumnWidth(idx, width)

        def add_item(self, event : KeyboardEventEx or mouse.MoveEvent or mouse.ButtonEvent):
            if isinstance(event, KeyboardEventEx):
                data_list = ["키보드", event.vk_code, event.scan_code, event.time]
            else:
                if isinstance(event, mouse.MoveEvent):
                    data_list = ["이동", event.x, event.y, event.time]

                elif isinstance(event, mouse.ButtonEvent):
                    data_list = ["클릭", event.event_type, event.button, event.time]

            cur_row_count = self.data_table.rowCount()
            new_row_count = cur_row_count + 1
            self.data_table.setRowCount(new_row_count)
            print(data_list)
            for idx, data in enumerate(data_list):
                item = QTableWidgetItem()
                item.setText(str(data))
                item.setData(Qt.UserRole, event)
                self.data_table.setItem(cur_row_count, idx, item)
                

        @Slot(object)
        def record_signal_handler(self, event : object):
            print(event)

        @Slot()
        def key_record_button_handler(self) -> None:
            if self.is_key_recorded:
                datas = self.recorder.key_record_stop()
                for data in datas:
                    self.add_item(data)
            else:
                self.recorder.key_record_start()

            self.is_key_recorded = not self.is_key_recorded
            self.key_record_button.setText("중지" if self.is_key_recorded else "키보드 녹화")

        @Slot()
        def mouse_record_button_handler(self) -> None:
            if self.is_mouse_recorded:
                datas = self.recorder.mouse_record_stop()
                for data in datas:
                    self.add_item(data)
            else:
                self.recorder.mouse_record_stop()

            self.is_mouse_recorded = not self.is_mouse_recorded

        @Slot()
        def key_mouse_record_button_handler(self) -> None:
            self.key_record_button.click()
            self.mouse_record_button.click()

        @Slot()
        def start_button_handler(self) -> None:
            row_count = self.data_table.rowCount()
            datas = [self.data_table.item(row_idx, 0).data(Qt.UserRole) for row_idx in range(row_count)]
            self.recorder.play(datas)


    app = QApplication(sys.argv)
    apply_stylesheet(app, theme = "dark_teal.xml")
    window = MainWindow()
    window.show()
    app.exec()
