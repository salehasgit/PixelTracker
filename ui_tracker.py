# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'tracker_ui.ui'
#
# Created: Tue Aug 23 02:01:25 2016
#      by: pyside-uic 0.2.15 running on PySide 1.2.2
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_mainWindow(object):
    def setupUi(self, mainWindow):
        mainWindow.setObjectName("mainWindow")
        mainWindow.resize(660, 599)
        self.centralwidget = QtGui.QWidget(mainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtGui.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.gridLayout = QtGui.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.widget = QtGui.QWidget(self.centralwidget)
        self.widget.setEnabled(True)
        self.widget.setObjectName("widget")
        self.goText = QtGui.QTextEdit(self.widget)
        self.goText.setEnabled(True)
        self.goText.setGeometry(QtCore.QRect(400, 510, 221, 61))
        self.goText.setTextInteractionFlags(QtCore.Qt.TextSelectableByKeyboard|QtCore.Qt.TextSelectableByMouse)
        self.goText.setObjectName("goText")
        self.image_label = QtGui.QLabel(self.widget)
        self.image_label.setGeometry(QtCore.QRect(0, 0, 641, 481))
        self.image_label.setObjectName("image_label")
        self.groupBox = QtGui.QGroupBox(self.widget)
        self.groupBox.setGeometry(QtCore.QRect(0, 500, 120, 80))
        self.groupBox.setCheckable(False)
        self.groupBox.setObjectName("groupBox")
        self.mode_1 = QtGui.QRadioButton(self.groupBox)
        self.mode_1.setGeometry(QtCore.QRect(10, 20, 101, 16))
        self.mode_1.setChecked(True)
        self.mode_1.setObjectName("mode_1")
        self.mode_2 = QtGui.QRadioButton(self.groupBox)
        self.mode_2.setGeometry(QtCore.QRect(10, 40, 91, 17))
        self.mode_2.setObjectName("mode_2")
        self.groupBox_2 = QtGui.QGroupBox(self.widget)
        self.groupBox_2.setGeometry(QtCore.QRect(130, 500, 91, 81))
        self.groupBox_2.setCheckable(False)
        self.groupBox_2.setObjectName("groupBox_2")
        self.calibrate = QtGui.QPushButton(self.groupBox_2)
        self.calibrate.setGeometry(QtCore.QRect(10, 20, 71, 41))
        self.calibrate.setObjectName("calibrate")
        self.gridLayout.addWidget(self.widget, 0, 0, 1, 1)
        self.verticalLayout.addLayout(self.gridLayout)
        mainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(mainWindow)
        QtCore.QMetaObject.connectSlotsByName(mainWindow)

    def retranslateUi(self, mainWindow):
        mainWindow.setWindowTitle(QtGui.QApplication.translate("mainWindow", "EyeWare", None, QtGui.QApplication.UnicodeUTF8))
        self.image_label.setText(QtGui.QApplication.translate("mainWindow", "ssss", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox.setTitle(QtGui.QApplication.translate("mainWindow", " processing modes", None, QtGui.QApplication.UnicodeUTF8))
        self.mode_1.setText(QtGui.QApplication.translate("mainWindow", "Mode 1", None, QtGui.QApplication.UnicodeUTF8))
        self.mode_2.setText(QtGui.QApplication.translate("mainWindow", "Mode 2", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox_2.setTitle(QtGui.QApplication.translate("mainWindow", "Callibration", None, QtGui.QApplication.UnicodeUTF8))
        self.calibrate.setText(QtGui.QApplication.translate("mainWindow", "callibrate", None, QtGui.QApplication.UnicodeUTF8))

