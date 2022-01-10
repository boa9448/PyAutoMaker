# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'input_form.ui'
##
## Created by: Qt User Interface Compiler version 6.2.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QGridLayout, QGroupBox, QHeaderView,
    QMainWindow, QMenuBar, QPushButton, QSizePolicy,
    QStatusBar, QTableWidget, QTableWidgetItem, QVBoxLayout,
    QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(807, 641)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.gridLayout_3 = QGridLayout(self.centralwidget)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.groupBox = QGroupBox(self.centralwidget)
        self.groupBox.setObjectName(u"groupBox")
        self.gridLayout_2 = QGridLayout(self.groupBox)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.data_table = QTableWidget(self.groupBox)
        self.data_table.setObjectName(u"data_table")

        self.gridLayout_2.addWidget(self.data_table, 0, 0, 1, 1)


        self.gridLayout_3.addWidget(self.groupBox, 0, 0, 1, 1)

        self.groupBox_2 = QGroupBox(self.centralwidget)
        self.groupBox_2.setObjectName(u"groupBox_2")
        self.gridLayout = QGridLayout(self.groupBox_2)
        self.gridLayout.setObjectName(u"gridLayout")
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.key_record_button = QPushButton(self.groupBox_2)
        self.key_record_button.setObjectName(u"key_record_button")
        sizePolicy = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.key_record_button.sizePolicy().hasHeightForWidth())
        self.key_record_button.setSizePolicy(sizePolicy)

        self.verticalLayout.addWidget(self.key_record_button)

        self.mouse_record_button = QPushButton(self.groupBox_2)
        self.mouse_record_button.setObjectName(u"mouse_record_button")
        sizePolicy.setHeightForWidth(self.mouse_record_button.sizePolicy().hasHeightForWidth())
        self.mouse_record_button.setSizePolicy(sizePolicy)

        self.verticalLayout.addWidget(self.mouse_record_button)

        self.key_mouse_record_button = QPushButton(self.groupBox_2)
        self.key_mouse_record_button.setObjectName(u"key_mouse_record_button")
        sizePolicy.setHeightForWidth(self.key_mouse_record_button.sizePolicy().hasHeightForWidth())
        self.key_mouse_record_button.setSizePolicy(sizePolicy)

        self.verticalLayout.addWidget(self.key_mouse_record_button)

        self.save_file_button = QPushButton(self.groupBox_2)
        self.save_file_button.setObjectName(u"save_file_button")
        sizePolicy.setHeightForWidth(self.save_file_button.sizePolicy().hasHeightForWidth())
        self.save_file_button.setSizePolicy(sizePolicy)

        self.verticalLayout.addWidget(self.save_file_button)

        self.load_file_button = QPushButton(self.groupBox_2)
        self.load_file_button.setObjectName(u"load_file_button")
        sizePolicy.setHeightForWidth(self.load_file_button.sizePolicy().hasHeightForWidth())
        self.load_file_button.setSizePolicy(sizePolicy)

        self.verticalLayout.addWidget(self.load_file_button)

        self.start_button = QPushButton(self.groupBox_2)
        self.start_button.setObjectName(u"start_button")
        sizePolicy.setHeightForWidth(self.start_button.sizePolicy().hasHeightForWidth())
        self.start_button.setSizePolicy(sizePolicy)

        self.verticalLayout.addWidget(self.start_button)


        self.gridLayout.addLayout(self.verticalLayout, 0, 0, 1, 1)


        self.gridLayout_3.addWidget(self.groupBox_2, 0, 1, 1, 1)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 807, 22))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.groupBox.setTitle(QCoreApplication.translate("MainWindow", u"\ub370\uc774\ud130", None))
        self.groupBox_2.setTitle(QCoreApplication.translate("MainWindow", u"\ubc84\ud2bc\uc784", None))
        self.key_record_button.setText(QCoreApplication.translate("MainWindow", u"\ud0a4\ubcf4\ub4dc \ub179\ud654", None))
        self.mouse_record_button.setText(QCoreApplication.translate("MainWindow", u"\ub9c8\uc6b0\uc2a4 \ub179\ud654", None))
        self.key_mouse_record_button.setText(QCoreApplication.translate("MainWindow", u"\ud0a4\ubcf4\ub4dc/\ub9c8\uc6b0\uc2a4 \ub179\ud654", None))
        self.save_file_button.setText(QCoreApplication.translate("MainWindow", u"\ud30c\uc77c\ub85c \uc800\uc7a5", None))
        self.load_file_button.setText(QCoreApplication.translate("MainWindow", u"\ud30c\uc77c\uc5d0\uc11c \ubd88\ub7ec\uc624\uae30", None))
        self.start_button.setText(QCoreApplication.translate("MainWindow", u"\uc2dc\uc791", None))
    # retranslateUi

