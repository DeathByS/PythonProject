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
from enums import Alarms, Machine, AbnormalSignAlarm, OptimizerData
import datetime
from pytz import timezone

from SingletonInstance import GetDataFromDB
import time
import os



class MainWindowAbnormalSignTab(QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)   
        print('init MainWindowAbnormalSignTab')
        # MainWindow 폼의 위젯을 조작할 것이기 때문에 MainWindow를 parent로 받아 MainWindow의 위젯을 조작함
        self.parent = parent

        self.alarmList = []
        # 알람 요인
        self.alarmCause = []  
        # 알람 횟수
        self.alarmCount = []
        
        # 현장의 오류로 인한 알람이 게속 뜨는걸 방지하기 위한 것
        self.alarmCheck = [False] * 5 

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
            alarmTime = datetime.datetime.strptime(i['timeData'], '%Y-%m-%dT%H:%M:%S.%f')
            alarmTime = alarmTime.strftime('%Y-%m-%d %H:%M')
            self.insertAlarm(i['alarm'], str(alarmTime))

        self.calcBaseData()
        
        self.timer = QTimer(self)
        self.timer.setInterval(1000 * 10)
        self.timer.start()
        self.timer.timeout.connect(self.insertAlarmList)

    def loadAlarmList(self):
        with open("data/AbnormalSign.txt", 'r', encoding='utf-8') as f:
           self.alarmList = f.readlines()


        print('alarmList')
        print(self.alarmList)  

    def calcBaseData(self):

        getData = GetDataFromDB.instance()

        current = datetime.datetime.now()
        ago = current - datetime.timedelta(days=3)
        # ago = current - datetime.timedelta(hours=1)
        baseLeftBalance = 0
        baseRightBalance = 0
        baseCoolingWaterTemp = 0
        baseTransformersTemp = 0
        # try:

        data = getData.getDataInRange('InfoData','timeData', str(ago), str(current),self.parent.machineName)
        length = len(data)
        # dcData = getData.getDataInRange('DCData','timeData', str(ago), str(current),self.parent.machineName)

        for i in data:

            baseLeftBalance += i['leftBalance']
            baseRightBalance += i['rightBalance']
            baseCoolingWaterTemp += i['drumcolingWater']
            baseTransformersTemp += i['transformersTemp']
            

        try:    
            print('baseData %f %f %f %f'%(baseLeftBalance/length,baseRightBalance/length,baseCoolingWaterTemp/length ,baseTransformersTemp/length))    

            # 사행 횟수 이상
            self.alarmCause.append((baseLeftBalance /length) * 1.5)
            self.alarmCause.append((baseRightBalance /length) * 1.5)

            # 온도 초과 이상
            self.alarmCause.append((baseCoolingWaterTemp /length) * 1.2)
            self.alarmCause.append((baseTransformersTemp /length) * 1.2)
            
        except:
            print('no data')
            pass
        
        # 고형물화수율 데이터 저장용으로 리스트 한 개 더 늘려놓음
        self.alarmCause.append(0)
        # except:
            # print('error')


    # 실시간으로 발생하고 있는 알람을 리스트에 추가함
    def insertAlarmList(self):
        
        currentTime = datetime.datetime.now()
        timeText = currentTime.strftime('%Y-%m-%d %H:%M')
        location = self.parent.machineName
        
        # 고형물회수율 계산용 데이터
        optimizeData = self.parent.plcConnect.readRegister(OptimizerData.AVGINPUTWATERRATE.value, 13)

        print('optimizeData')
        print(optimizeData)


        # 
        data = self.parent.plcConnect.readRegister(self.parent.machineStartReg + Regs.DRUMFRQ.value, 
                                                        Regs.KW.value + 1)

        currentData = []
        currentData.append(data[Regs.LEFTBALANCE.value])
        currentData.append(data[Regs.RIGHTBALANCE.value])
        currentData.append(data[Regs.DRUMCOLLINGWATER.value] / 10)
        currentData.append(data[Regs.TRANSFORMERSTEMP.value]/ 10)
        currentData.append(0.92)

        print('CurrentData')
        print(currentData)


        # 고형물회수율
        try:
            solidsCaptureRate = (
            (
                (optimizeData[OptimizerData.AVGSLUDGEOUTPUT.value - 3000] / optimizeData[OptimizerData.AVGSLUDGEINPUT.value - 3000])) /
                ((1 - (optimizeData[OptimizerData.AVGINPUTWATERRATE.value - 3000] /100)) / (1 - (optimizeData[OptimizerData.AVGOUTPUTWATERRATE.value - 3000])/100))
            )
        except ZeroDivisionError:
            solidsCaptureRate = 0.0
        
        self.alarmCause[len(self.alarmCause) -1] = solidsCaptureRate

        print('alarmCause')
        print(self.alarmCause)

        for i in range(0, len(self.alarmCause)):

            if(currentData[i] > self.alarmCause[i]):    
                if(self.alarmCheck[i] == False):
                    self.alarmCheck[i] = True

                    alarmCauseText = self.alarmList[i]

                    self.insertAlarm(alarmCauseText, timeText)
               
                    self.showMessageBox(alarmCauseText, i)

                    alarmtime = datetime.datetime.now()
                    with open("log/AbnormalSignAlarmLog.txt", "at", encoding='utf-8') as f:
                        f.write(str(alarmtime) + ' %s %s\n'%(location, alarmCauseText))

                    # self.numberOfAlarm += 1
                    self.parent.setNumberOfAbnormalSignAlarm(1)
            else:
                if(self.alarmCheck[i] == True):
                    self.alarmCheck[i] = False
            

        
            
         
        # with open("log/AbnormalSignAlarmLog.txt", "at", encoding='utf-8') as f:
        #     f.write(str(currentTime) + ' %s %s\n'%(location, alarmCauseText))


               

    # 다른 탭 ex)이상징후, 교체주기 에서 직접 알람을 추가할 때 사용 
    def insertAlarm(self, text='', alarmTime ='', alarmCountText =''):
        
        if(alarmTime == ''):
            currentTime = datetime.datetime.now()
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
        msgbox.setModal(False)
        msgbox.setStandardButtons(QtWidgets.QMessageBox.Yes)
        msgboxYesBtn = msgbox.button(QtWidgets.QMessageBox.Yes)
        msgboxYesBtn.setText("확인")

        # ret = msgbox.exec_()
        ret = msgbox.show()

    
       



