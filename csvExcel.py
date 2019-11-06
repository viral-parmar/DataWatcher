# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'csvExcel.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
import os
from Main_File import Watcher, DataFrameTableWidget
import pandas as pd

pd.set_option('precision', 2)

class Ui_MainWindow(object):

    def __init__(self):

        self.file_Name = None

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.gridLayout_2 = QtWidgets.QGridLayout()
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.start_button = QtWidgets.QPushButton(self.centralwidget)
        self.start_button.setAutoFillBackground(False)
        self.start_button.setAutoDefault(False)
        self.start_button.setDefault(False)
        self.start_button.setFlat(False)
        self.start_button.setObjectName("start_button")
        self.gridLayout_2.addWidget(self.start_button, 0, 0, 1, 1)
        self.Br_button = QtWidgets.QPushButton(self.centralwidget)
        self.Br_button.setObjectName("Br_button")
        self.Br_button.clicked.connect(lambda: self.browse_button())
        self.gridLayout_2.addWidget(self.Br_button, 2, 0, 1, 1)
        self.label = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.gridLayout_2.addWidget(self.label, 2, 1, 1, 1, QtCore.Qt.AlignHCenter)
        self.tableWidget = DataFrameTableWidget(self.centralwidget)
        self.tableWidget.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(0)
        self.tableWidget.setRowCount(0)
        self.gridLayout_2.addWidget(self.tableWidget, 3, 0, 1, 2)
        self.gridLayout.addLayout(self.gridLayout_2, 0, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.start_button.setToolTip(_translate("MainWindow", "Start The Program"))
        self.start_button.setText(_translate("MainWindow", "Start"))
        self.Br_button.setToolTip(_translate("MainWindow", "Browse the File Location to Watch on"))
        self.Br_button.setText(_translate("MainWindow", "Browse"))
        self.label.setText(_translate("MainWindow", "Sensor CSV To Excel"))


class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)
        self.start_button.clicked.connect(self.start_button_click)
        self.watcher = Watcher()
        self.watcher.emitter.newDataFrameSignal.connect(self.tableWidget.append_dataframe)
        self.file_Name = ""

    def start_button_click(self):
        self.watcher.set_filename(self.file_Name)
        if self.start_button.text() == "Start":
            self.start_button.setText("Stop")
            self.watcher.run()
        elif self.start_button.text() == "Stop":
            self.start_button.setText("Start")
            self.watcher.stop_watcher()

    def browse_button(self):
        self.file_Name = QtWidgets.QFileDialog.getExistingDirectory(None, 'Open working directory', os.getcwd(), QtWidgets.QFileDialog.ShowDirsOnly)
        print(self.file_Name)


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    # MainWindow = QtWidgets.QMainWindow()
    # ui = Ui_MainWindow()
    # ui.setupUi(MainWindow)
    # MainWindow.show()
    w = MainWindow()
    w.show()

    sys.exit(app.exec_())

