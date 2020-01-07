# coding: utf-8
 
import sys
import csv

from PyQt5 import QtWidgets
from PyQt5 import uic
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtCore import QModelIndex
from MainWindowTab1 import MainWindowTab1


 
class MainWindow(QtWidgets.QDialog):
    def __init__(self, parent=None):
        QtWidgets.QDialog.__init__(self, parent)
        self.ui = uic.loadUi("MainForm.ui")
        # self.ui.tabWidget.addTab(MainWindowTab1(), MainWindowTab1.__name__)
        # self.ui.tabWidget.addTab(MainWindowTab1(), MainWindowTab1.__name__)
       
        # 메인윈도우에 실린 위젯을 조작하기 위해서, 메인윈도우를 부모로 보내어 다른 클래스에서 조작할 수 있게 만든다.
        self.mainWindowTab1 = MainWindowTab1(self)
        # MainWindowTab1.init_widget(self)



if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    w = MainWindow()
    sys.exit(app.exec())