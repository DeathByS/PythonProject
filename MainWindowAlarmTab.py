# coding: utf-8

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QTabWidget
from PyQt5.QtWidgets import QTableWidget
from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtCore import QModelIndex
from PyQt5.QtCore import QTimer
from enums import Regs
from enums import Alarms, Machine
from datetime import datetime
import time
import pickle
from SingletonInstance import GetDataFromDB
from SingletonInstance import EmailSender


class MainWindowAlarmTab(QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)   
        
        # MainWindow 폼의 위젯을 조작할 것이기 때문에 MainWindow를 parent로 받아 MainWindow의 위젯을 조작함
        self.parent = parent

        self.alarmList = {}
        # 알람 요인
        self.alarmCause = []  
        # 알람 횟수
        self.alarmCount = []
        
        # 현장의 오류로 인한 알람이 게속 뜨는걸 방지하기 위한 것
        self.alarmCheck = []

        for i in range(0, Alarms.ENDLIST.value + 1):
            self.alarmCheck.append(0)

        print(self.alarmCheck)    

        self.parent.tableWidget.setColumnWidth(0,250)
        self.parent.tableWidget.setColumnWidth(1,500)
        self.parent.tableWidget.setColumnWidth(2,150)
        
        self.loadAlarmList()

        alarmData = GetDataFromDB.instance().getDataAll('AlarmData', self.parent.machineName)

        for i in alarmData:
            alarmTime = datetime.strptime(i['timeData'], '%Y-%m-%dT%H:%M:%S.%f')
            alarmTime = alarmTime.strftime('%Y-%m-%d %H:%M')
            self.insertAlarm(i['alarm'], str(alarmTime))

        self.numberOfAlarm = 0
        
        self.timer = QTimer(self)
        self.timer.setInterval(10000)
        self.timer.start()
        self.timer.timeout.connect(self.insertAlarmList)
        
        self.timer2 = QTimer(self)
        self.timer2.setInterval(1000 * 60 * 10)
        self.timer2.start()
        self.timer2.timeout.connect(self.sludgeOutCheck)

    def loadAlarmList(self):
        with open('data/AlarmList.bin', 'rb') as f:
           self.alarmList = pickle.load(f)

        #    print(self.alarmList[Alarms.PANELEMERGENCYSTOP.name])  

    # 실시간으로 발생하고 있는 알람을 리스트에 추가함
    def insertAlarmList(self):
        
        currentTime = datetime.now()
        timeText = currentTime.strftime('%Y-%m-%d %H:%M')
        
        # 알람 요인, 알람 횟수
        
        self.alarmCause = self.parent.plcConnect.readCoil(self.parent.machineStartCoil + Alarms.PANELEMERGENCYSTOP.value, 
                                                            Alarms.ENDLIST.value + 1)
        self.alarmCount = self.parent.plcConnect.readRegister(self.parent.machineStartReg + Alarms.PANELEMERGENCYSTOP.value
                                                             + Machine.ALARMCOUNTSTART.value, Alarms.ENDLIST.value + 1)
        # print(self.alarmCause)
        for i in Alarms:
            
            if(self.alarmCause[i.value]):
                if(self.alarmCheck[i.value] == False):
                    self.alarmCheck[i.value] = True
 
                    # 알람 발생 요인 item 추가 alarmList[1] = plc 주소, alarmList[0] = 알람 내용
                    alarmCauseText = "["+self.alarmList[i.name][1]+"]" + " " + self.alarmList[i.name][0]
                  
                    alarmCountText = str(self.alarmCount[i.value])

                    self.insertAlarm(alarmCauseText, timeText, alarmCountText)
               
                    self.showMessageBox(alarmCauseText, i.value)

                    self.numberOfAlarm += 1
            else:
                if(self.alarmCheck[i.value] == True):
                    self.alarmCheck[i.value] = False
                    self.numberOfAlarm -= 1

            # 운전 현황 탭의 알람 표시용 
            self.parent.setNumberOfAlarm(self.numberOfAlarm)    

    # 다른 탭 ex)이상징후, 교체주기 에서 직접 알람을 추가할 때 사용 
    def insertAlarm(self, text='', alarmTime ='', alarmCountText =''):
        
        if(alarmTime == ''):
            currentTime = datetime.now()
            timeText = currentTime.strftime('%Y-%m-%d %H:%M')
        else:
            timeText = alarmTime    

        self.parent.tableWidget.insertRow(0)

        item = []
        item.append(QTableWidgetItem(timeText))
        item.append(QTableWidgetItem(text))
        item.append(QTableWidgetItem(alarmCountText))
        
        for j in range(self.parent.tableWidget.columnCount()):
            self.parent.tableWidget.setItem(0, j, item[j])

        # self.showMessageBox(text, 1)            

    def showMessageBox(self, text, number = 0):
        msgbox = QtWidgets.QMessageBox(self)
        msgbox.setObjectName('msgbox')
        # msgbox.setStyleSheet('QMessageBox#msgbox {background-image: url(:/image/label4.png) }')
        # msgbox.setStyleSheet("QLabel{ color: white}")
        # msgbox.setStyleSheet("QLabel{min-width:500 px; font-size: 24px;")
        msgbox.setWindowTitle('알람 발생')
        msgbox.setText(text)
        msgbox.setStandardButtons(QtWidgets.QMessageBox.Yes)
        msgboxYesBtn = msgbox.button(QtWidgets.QMessageBox.Yes)
        msgboxYesBtn.setText("확인")
        msgboxYesBtn.setStyleSheet('QMessageBox#msgbox {background-image: url(:/image/label4.png) }')

        ret = msgbox.exec_()

    
        # if ret == QtWidgets.QMessageBox.Yes:
            # print('yes' + str(number))
            # self.parent.plcConnect.writeCoils(Machine.EXCALARMSWITCHSTART.value, 1)

            # if(number in range(Alarms.DRUMEXC.value, Alarms.FILTEREXC.value + 1, 1)):
            #     print("SENDMSG")
            #     switch = [False] * 6
            #     switch[number - Alarms.DRUMEXC.value] = True
            #     print("MSG : " + str(switch))
            #     self.parent.plcConnect.writeCoils(Machine.EXCALARMSWITCHSTART.value, switch)
                
                # switch[number - Alarms.DRUMEXC.value] = False
                # self.parent.plcConnect.writeCoils(Machine.EXCALARMSWITCHSTART.value, switch)


        # msgbox.question(self, 'MessageBox title', 'Here comes message', msgboxYesBtn)


    def sludgeOutCheck(self):
        
        try:
            sludgeCheck = self.parent.plcConnect.readCoil(144, 1)

            if(sludgeCheck[0]):

                emailSender = EmailSender.instance()
                emailReciver = self.parent.lineEdit_sludgeOutEmail.text()

                location = self.parent.machineName

                subject = '%s 배출 슬러지 배차 알람 메일 입니다'%location
                msg = '슬러지 량이 설정된 값을 초과하여 배출 알림 메일을 보냅니다.'
                emailSender.emailSend(reciver=emailReciver,subject=subject, msg=msg)
                Time = datetime.now()

                with open("log/SludgeOutEmailSendLog.txt", "at", encoding='utf-8') as f:
                    f.write(str(Time) + ' %s 슬러지 배출 알람 이메일 발송\n'%location)

                self.parent.setNumberOfOfSludgeOutAlarm(1)

                

        except:
            print('error : sludgeOut check part, MainWindowAlarm')
            return 

