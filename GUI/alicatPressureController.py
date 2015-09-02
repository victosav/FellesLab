# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'alicatPressureController.ui'
#
# Created: Wed Sep  2 13:38:28 2015
#      by: PyQt4 UI code generator 4.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(767, 391)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.pushButton_setpoint = QtGui.QPushButton(self.centralwidget)
        self.pushButton_setpoint.setGeometry(QtCore.QRect(359, 40, 131, 32))
        self.pushButton_setpoint.setObjectName(_fromUtf8("pushButton_setpoint"))
        self.label = QtGui.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(120, 110, 56, 13))
        self.label.setObjectName(_fromUtf8("label"))
        self.label_2 = QtGui.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(260, 110, 56, 13))
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.label_3 = QtGui.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(420, 110, 56, 13))
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.label_4 = QtGui.QLabel(self.centralwidget)
        self.label_4.setGeometry(QtCore.QRect(270, 30, 56, 13))
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.label_5 = QtGui.QLabel(self.centralwidget)
        self.label_5.setGeometry(QtCore.QRect(130, 30, 56, 13))
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.lineEdit_message = QtGui.QLineEdit(self.centralwidget)
        self.lineEdit_message.setGeometry(QtCore.QRect(120, 80, 361, 22))
        self.lineEdit_message.setReadOnly(True)
        self.lineEdit_message.setObjectName(_fromUtf8("lineEdit_message"))
        self.lineEdit_setpoint = QtGui.QLineEdit(self.centralwidget)
        self.lineEdit_setpoint.setGeometry(QtCore.QRect(120, 50, 113, 22))
        self.lineEdit_setpoint.setObjectName(_fromUtf8("lineEdit_setpoint"))
        self.label_6 = QtGui.QLabel(self.centralwidget)
        self.label_6.setGeometry(QtCore.QRect(270, 50, 56, 13))
        self.label_6.setObjectName(_fromUtf8("label_6"))
        self.label_7 = QtGui.QLabel(self.centralwidget)
        self.label_7.setGeometry(QtCore.QRect(120, 140, 56, 13))
        self.label_7.setObjectName(_fromUtf8("label_7"))
        self.label_8 = QtGui.QLabel(self.centralwidget)
        self.label_8.setGeometry(QtCore.QRect(120, 170, 56, 13))
        self.label_8.setObjectName(_fromUtf8("label_8"))
        self.label_9 = QtGui.QLabel(self.centralwidget)
        self.label_9.setGeometry(QtCore.QRect(120, 200, 56, 13))
        self.label_9.setObjectName(_fromUtf8("label_9"))
        self.label_10 = QtGui.QLabel(self.centralwidget)
        self.label_10.setGeometry(QtCore.QRect(420, 130, 56, 13))
        self.label_10.setObjectName(_fromUtf8("label_10"))
        self.label_11 = QtGui.QLabel(self.centralwidget)
        self.label_11.setGeometry(QtCore.QRect(420, 190, 56, 13))
        self.label_11.setObjectName(_fromUtf8("label_11"))
        self.label_12 = QtGui.QLabel(self.centralwidget)
        self.label_12.setGeometry(QtCore.QRect(420, 160, 56, 13))
        self.label_12.setObjectName(_fromUtf8("label_12"))
        self.lineEdit_pressure = QtGui.QLineEdit(self.centralwidget)
        self.lineEdit_pressure.setGeometry(QtCore.QRect(250, 130, 113, 22))
        self.lineEdit_pressure.setObjectName(_fromUtf8("lineEdit_pressure"))
        self.lineEdit_temperature = QtGui.QLineEdit(self.centralwidget)
        self.lineEdit_temperature.setGeometry(QtCore.QRect(250, 160, 113, 22))
        self.lineEdit_temperature.setObjectName(_fromUtf8("lineEdit_temperature"))
        self.lineEdit_3 = QtGui.QLineEdit(self.centralwidget)
        self.lineEdit_3.setGeometry(QtCore.QRect(250, 190, 113, 22))
        self.lineEdit_3.setObjectName(_fromUtf8("lineEdit_3"))
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 767, 22))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        self.menuAlicat_Pressure_controller = QtGui.QMenu(self.menubar)
        self.menuAlicat_Pressure_controller.setObjectName(_fromUtf8("menuAlicat_Pressure_controller"))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        MainWindow.setStatusBar(self.statusbar)
        self.menubar.addAction(self.menuAlicat_Pressure_controller.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow", None))
        self.pushButton_setpoint.setText(_translate("MainWindow", "confirm setpoint", None))
        self.label.setText(_translate("MainWindow", "Variable", None))
        self.label_2.setText(_translate("MainWindow", "Value", None))
        self.label_3.setText(_translate("MainWindow", "Unit", None))
        self.label_4.setText(_translate("MainWindow", "Unit", None))
        self.label_5.setText(_translate("MainWindow", "Set Point", None))
        self.label_6.setText(_translate("MainWindow", "[bar]", None))
        self.label_7.setText(_translate("MainWindow", "Pressue", None))
        self.label_8.setText(_translate("MainWindow", "Temperature", None))
        self.label_9.setText(_translate("MainWindow", "Flow", None))
        self.label_10.setText(_translate("MainWindow", "[bar]", None))
        self.label_11.setText(_translate("MainWindow", "[l/min]", None))
        self.label_12.setText(_translate("MainWindow", "[C]", None))
        self.menuAlicat_Pressure_controller.setTitle(_translate("MainWindow", "Alicat Pressure controller", None))

