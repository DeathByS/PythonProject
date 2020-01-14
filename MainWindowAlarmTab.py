# coding: utf-8

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QTabWidget
from PyQt5 import uic
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtCore import QModelIndex
from PyQt5.QtCore import QTimer
from enums import Regs
import time
import pickle

class MainWindowAlarmTab(QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)   
        
        # MainWindow 폼의 위젯을 조작할 것이기 때문에 MainWindow를 parent로 받아 MainWindow의 위젯을 조작함
        self.parent = parent
        self.alarmList = {}
        
        # tableWidget->horizontalHeader()->setSectionResizeMode(QHeaderView::ResizeToContents);
        self.parent.tableWidget.setColumnWidth(0,parent.tableWidget.width()/4)
        self.parent.tableWidget.setColumnWidth(1,parent.tableWidget.width()/4)
        self.parent.tableWidget.setColumnWidth(2,parent.tableWidget.width()/4)

        # self.initWidget()

        # self.timer = QTimer(self)
        # self.timer.setInterval(3000)
        # self.timer.start()
        # # self.timer.timeout.connect(self.changeLcdNumber)

    def loadAlarmList(self):
        with open('AlarmList.bin', 'rb') as f:
           self.alarmList = pickle.load(f)

           print(self.alarmList)  

    # def initWidget(self):
       
        
    # def changeLcdNumber(self):
    
        

              




        