# coding: utf-8

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QTabWidget
from PyQt5 import uic
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtCore import QModelIndex
from PyQt5.QtCore import QTimer
import time

class MainWindowTab1(QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)   
        
        # MainWindow 폼의 위젯을 조작할 것이기 때문에 MainWindow를 parent로 받아 MainWindow의 위젯을 조작함
        self.parent = parent
        self.lcdList = []
        self.initWidget()

        self.timer = QTimer(self)
        self.timer.setInterval(5000)
        self.timer.start()
        self.timer.timeout.connect(self.changeLcdNumber)
        
    def initWidget(self):
        self.lcdList.append(self.parent.lcdNumber_1)
        self.lcdList.append(self.parent.lcdNumber_2)
        self.lcdList.append(self.parent.lcdNumber_3)
        self.lcdList.append(self.parent.lcdNumber_4)
        self.lcdList.append(self.parent.lcdNumber_5)
        self.lcdList.append(self.parent.lcdNumber_6)
        self.lcdList.append(self.parent.lcdNumber_7)
        self.lcdList.append(self.parent.lcdNumber_8)
        self.lcdList.append(self.parent.lcdNumber_9)
        self.lcdList.append(self.parent.lcdNumber_10)
        self.lcdList.append(self.parent.lcdNumber_11)
        
    def changeLcdNumber(self):
    
        coils, regs = self.parent.plcConnect.readPlcData()
        # colis2, regs2 = self.parent.plcConnect2.readPlcData()
       
        if coils == 'read error' or regs == 'read error':
            self.timer.stop()
            print("read error, check Connect ")
            return "error"
             
        else:
            # self.parent.plcWriteObject1.writePlcData(0, regs)
            # self.parent.plcWriteObject1.writePlcData(20,regs2)   
            for i in range(11):
                self.lcdList[i].display(float(regs[i]))




        