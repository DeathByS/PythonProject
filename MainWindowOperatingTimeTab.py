# coding: utf-8

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QTabWidget
from PyQt5 import uic
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtCore import QModelIndex
from PyQt5.QtCore import QTimer
from enums import OperatingTime
import time

class MainWindowOperatingTimeTab(QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)   
        
        # MainWindow 폼의 위젯을 조작할 것이기 때문에 MainWindow를 parent로 받아 MainWindow의 위젯을 조작함
        self.parent = parent
        self.timeLableList = []
        self.initWidget()
        self.timer = QTimer(self)
        self.timer.setInterval(10000)
        self.timer.start()
        self.timer.timeout.connect(self.changeTimeLabel)
        
    def initWidget(self):

        self.timeLableList.append(self.parent.label_Time_1)
        self.timeLableList.append(self.parent.label_Time_2)
        self.timeLableList.append(self.parent.label_Time_3)
        self.timeLableList.append(self.parent.label_Time_4)
        self.timeLableList.append(self.parent.label_Time_5)
        self.timeLableList.append(self.parent.label_Time_6)
        self.timeLableList.append(self.parent.label_Time_7)

    def changeTimeLabel(self):

        timeList = self.parent.plcConnect.readRegister(self.parent.machineStartReg + OperatingTime.TOTALMIN.value, 
                                                        OperatingTime.FILTERHOUR.value - OperatingTime.TOTALMIN.value + 1)

        timeListIndex = 0

        print(timeList)
        
        for i in range(1, OperatingTime.FILTERHOUR.value - OperatingTime.TOTALMIN.value + 2, 2):
            print(i)
            timeText = str(timeList[i]) +"시간 " + str(timeList[i-1]) +"분" 
            self.timeLableList[timeListIndex].setText(timeText)
            timeListIndex = timeListIndex + 1 

