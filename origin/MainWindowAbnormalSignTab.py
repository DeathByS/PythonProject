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
from enums import Alarms, Machine, AbnormalSignAlarm
from datetime import datetime
from SingletonInstance import GetDataFromDB
import time



class MainWindowAbnormalSignTab(QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)   
        
        # MainWindow 폼의 위젯을 조작할 것이기 때문에 MainWindow를 parent로 받아 MainWindow의 위젯을 조작함
        self.parent = parent

        self.alarmList = []
        # 알람 요인
        self.alarmCause = []  
        # 알람 횟수
        self.alarmCount = []
        
        # 현장의 오류로 인한 알람이 게속 뜨는걸 방지하기 위한 것
        self.alarmCheck = []

        for i in range(0, AbnormalSignAlarm.ENDLIST.value + 1):
            self.alarmCheck.append(0)

        print(self.alarmCheck)    

        self.parent.tableWidget_2.setColumnWidth(0,250)
        self.parent.tableWidget_2.setColumnWidth(1,500)
        self.parent.tableWidget_2.setColumnWidth(2,150)
        
        self.loadAlarmList()
        self.numberOfAlarm = 0


        alarmData = GetDataFromDB.instance().getDataAll('AbnormalSignData', self.parent.machineName)

        for i in alarmData:
            alarmTime = datetime.strptime(i['timeData'], '%Y-%m-%dT%H:%M:%S.%f')
            alarmTime = alarmTime.strftime('%Y-%m-%d %H:%M')
            self.insertAlarm(i['alarm'], str(alarmTime))

        
        self.timer = QTimer(self)
        self.timer.setInterval(10000)
        self.timer.start()
        self.timer.timeout.connect(self.insertAlarmList)

    def loadAlarmList(self):
        with open("data/AbnormalSign.txt", 'r', encoding='utf-8') as f:
           self.alarmList = f.readlines()


        print('alarmList')
        print(self.alarmList)  

    # 실시간으로 발생하고 있는 알람을 리스트에 추가함
    def insertAlarmList(self):
        
        currentTime = datetime.now()
        timeText = currentTime.strftime('%Y-%m-%d %H:%M')
        
        # 알람 요인, 알람 횟수
        try:
            self.alarmCause = self.parent.plcConnect.readCoil(self.parent.machineStartCoil + AbnormalSignAlarm.OUTOFTIME.value, 
                                                            AbnormalSignAlarm.ENDLIST.value - AbnormalSignAlarm.OUTOFTIME.value + 1)
        # self.alarmCount = self.parent.plcConnect.readRegister(self.parent.machineStartReg + Alarms.PANELEMERGENCYSTOP.value
        #                                                      + Machine.ALARMCOUNTSTART.value, Alarms.ENDLIST.value + 1)
        except:
            print('error abnomalSign')
            return
        location = self.parent.machineName
        print('Abnormal')
        print(self.alarmCause)
        
        for i in range(0, AbnormalSignAlarm.ENDLIST.value - AbnormalSignAlarm.OUTOFTIME.value + 1) :
            
            if(self.alarmCause[i]):
                if(self.alarmCheck[i] == False):
                    self.alarmCheck[i] = True

                    alarmCauseText = self.alarmList[i]

                    self.insertAlarm(alarmCauseText, timeText)
               
                    self.showMessageBox(alarmCauseText, i)

                    alarmtime = datetime.now()
                    with open("log/AbnormalSignAlarmLog.txt", "at", encoding='utf-8') as f:
                        f.write(str(alarmtime) + ' %s %s\n'%(location, alarmCauseText))

                    # self.numberOfAlarm += 1
                    self.parent.setNumberOfAbnormalSignAlarm(1)
            else:
                if(self.alarmCheck[i] == True):
                    self.alarmCheck[i] = False
                    # self.numberOfAlarm -= 1

               

    # 다른 탭 ex)이상징후, 교체주기 에서 직접 알람을 추가할 때 사용 
    def insertAlarm(self, text='', alarmTime ='', alarmCountText =''):
        
        if(alarmTime == ''):
            currentTime = datetime.now()
            timeText = currentTime.strftime('%Y-%m-%d %H:%M')
        else:
            timeText = alarmTime    

        self.parent.tableWidget_2.insertRow(0)

        item = []
        item.append(QTableWidgetItem(timeText))
        item.append(QTableWidgetItem(text))
        item.append(QTableWidgetItem(alarmCountText))
        
        for j in range(self.parent.tableWidget_2.columnCount()):
            self.parent.tableWidget_2.setItem(0, j, item[j])

        # self.showMessageBox(text, 1)            

    def showMessageBox(self, text, number):
        msgbox = QtWidgets.QMessageBox(self)
        # msgbox.setStyleSheet("QLabel{min-width:500 px; font-size: 24px;")
        msgbox.setWindowTitle('알람 발생')
        msgbox.setText(text)
        msgbox.setStandardButtons(QtWidgets.QMessageBox.Yes)
        msgboxYesBtn = msgbox.button(QtWidgets.QMessageBox.Yes)
        msgboxYesBtn.setText("확인")

        ret = msgbox.exec_()

    
       



