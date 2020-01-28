# coding: utf-8

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QTabWidget
from PyQt5.QtWidgets import QTableWidget
from PyQt5.QtWidgets import QTableWidgetItem
from PyQt5 import uic
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtCore import QModelIndex
from PyQt5.QtCore import QTimer
from enums import Regs
from enums import Alarms, Machine
from datetime import datetime
import time
import pickle

class MainWindowAlarmTab(QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)   
        
        # MainWindow 폼의 위젯을 조작할 것이기 때문에 MainWindow를 parent로 받아 MainWindow의 위젯을 조작함
        self.parent = parent
        self.alarmList = {}
        self.alarmCause = []
        self.alarmCount = []
        
        
        self.parent.tableWidget.setColumnWidth(0,250)
        self.parent.tableWidget.setColumnWidth(1,500)
        self.parent.tableWidget.setColumnWidth(2,150)
        
        self.loadAlarmList()
        
        self.timer = QTimer(self)
        self.timer.setInterval(10000)
        self.timer.start()
        self.timer.timeout.connect(self.insertAlarmList)

    def loadAlarmList(self):
        with open('AlarmList.bin', 'rb') as f:
           self.alarmList = pickle.load(f)

           print(self.alarmList[Alarms.PANELEMERGENCYSTOP.name])  

    def insertAlarmList(self):
        # 알람 발생 시간
        time = datetime.now()
        timeText = time.strftime('%Y-%m-%d %H:%M')

        # 알람 요인, 알람 횟수
        self.alarmCause = self.parent.plcConnect.readCoil(self.parent.machineStartCoil + Alarms.PANELEMERGENCYSTOP.value, 
                                                            Alarms.ENDLIST.value)
        self.alarmCount = self.parent.plcConnect.readRegister(self.parent.machineStartReg + Alarms.PANELEMERGENCYSTOP.value
                                                             + Machine.ALARMCOUNTSTART.value, Alarms.ENDLIST.value)
        # print(self.alarmCause)
        for i in Alarms:
            
            if(self.alarmCause[i.value]):
                
                self.parent.tableWidget.insertRow(0)
                item = []
                item.append(QTableWidgetItem(timeText))
                # 알람 발생 요인 item 추가 alarmList[1] = plc 주소, alarmList[0] = 알람 내용
                alarmCauseText = "["+self.alarmList[i.name][1]+"]" + " " + self.alarmList[i.name][0]
                item.append(QTableWidgetItem(alarmCauseText))
                alarmCountText = str(self.alarmCount[i.value])
                item.append(QTableWidgetItem(alarmCountText))
            
                for j in range(0, self.parent.tableWidget.columnCount()):
                     self.parent.tableWidget.setItem(0, j, item[j])
                
                print(i)
                self.showMessageBox(alarmCauseText, i.value)

    def showMessageBox(self, text, number):
        msgbox = QtWidgets.QMessageBox(self)
        # msgbox.setStyleSheet("QLabel{min-width:500 px; font-size: 24px;")
        msgbox.setWindowTitle('알람 발생')
        msgbox.setText(text)
        msgbox.setStandardButtons(QtWidgets.QMessageBox.Yes)
        msgboxYesBtn = msgbox.button(QtWidgets.QMessageBox.Yes)
        msgboxYesBtn.setText("확인")

        ret = msgbox.exec_()

        if ret == QtWidgets.QMessageBox.Yes:
            print('yes' + str(number))
            self.parent.plcConnect.writeCoils(Machine.EXCALARMSWITCHSTART.value, 1)

            if(number in range(Alarms.DRUMEXC.value, Alarms.FILTEREXC.value + 1, 1)):
                print("SENDMSG")
                switch = [False] * 6
                switch[number - Alarms.DRUMEXC.value] = True
                print("MSG : " + str(switch))
                self.parent.plcConnect.writeCoils(Machine.EXCALARMSWITCHSTART.value, switch)
                
                # switch[number - Alarms.DRUMEXC.value] = False
                # self.parent.plcConnect.writeCoils(Machine.EXCALARMSWITCHSTART.value, switch)


        # msgbox.question(self, 'MessageBox title', 'Here comes message', msgboxYesBtn)
    # def initWidget(self):
       
        
    # def changeLcdNumber(self):
    
    