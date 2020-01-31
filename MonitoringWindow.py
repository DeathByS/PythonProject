# coding: utf-8
 
import sys
import csv

from PyQt5 import QtWidgets, QtGui
from PyQt5 import uic
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtCore import QModelIndex
from sync_Client import SyncClient 
from PyQt5.QtGui import QFont
from PyQt5.QtCore import QTimer
from enums import Coils, Machine, Regs, Monitoring
from MainWindow import MainWindow
 
class MonitoringWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('MonitoringForm.ui', self)

        # 연결 위치 : key, Plc Connection Object : Value
        self.plcConnectDict = {} 
        self.ip = None
        
        self.statusLabelList = []
        self.locationButtonList = []

        self.connectListDict = {}

        self.initConnectionList()
        self.initStatusLabel()
        self.initLocationButton()

        self.initPlcConnect()

        self.changeStatusLabel()

        self.timer = QTimer(self)
        self.timer.setInterval(10000)
        self.timer.start()
        self.timer.timeout.connect(self.changeStatusLabel)
        

    def initConnectionList(self):
    
        with open('ConnectionList.csv', 'r', encoding='utf-8') as f:
            rdr = csv.reader(f)
            
            connList = [] 
            
            for row in rdr:
                 connList.append(row)
                #  print(connList)
                #  self.connectListBox.addItem(row[0])

            self.connectListDict = dict(connList)
            # print(self.connectListDict)

    def initPlcConnect(self):
            # 딕셔너리의 키만 받아서 리스트 같이 사용
        for i in self.connectListDict.keys():
            self.plcConnectDict[i] = (self.connect(self.connectListDict[i]))


    def initStatusLabel(self):
        
        for i in range(1, Monitoring.NUMBEROFLABELS.value + 1):
            # 오브젝트의 이름을 가지고 오브젝트 찾아 사용하는법.
            labelName = "label_%d" % i
            self.statusLabelList.append(self.findChild(QtWidgets.QLabel, labelName))

    def initLocationButton(self):
        for i in range(1, Monitoring.NUMBEROFBUTTONS.value + 1):
            # 오브젝트의 이름을 가지고 오브젝트 찾아 사용하는법.
            buttonName = "pushButton_%d" % i
            self.locationButtonList.append(self.findChild(QtWidgets.QPushButton, buttonName))

        for i in self.locationButtonList:
            i.clicked.connect(lambda state, button=i : self.slotConnectButton(state, button))


    def connect(self, ip = "kwtkorea.iptime.org"):
        plcConnect = SyncClient()
        plcConnect.connectClient(ip, 502)
        return plcConnect

    def changeStatusLabel(self):
        print("changes")
        

        dataList = []


        
        for j in range(4): 
            
            location, machineStartReg, machineStartCoil = self.setLocation(self.locationButtonList[j].text())
            onoff = self.plcConnectDict[location].readCoil(machineStartCoil + Coils.AUTOMATICSTART.value, 1)
            dcV = self.plcConnectDict[location].readRegister(machineStartReg + Regs.DCV.value, 1)
            dcA = self.plcConnectDict[location].readRegister(machineStartReg + Regs.DCA.value, 1)
            alarm = self.plcConnectDict[location].readCoil(machineStartCoil + Coils.REMOTESTOP.value, 1)
            
            dataList.append(onoff)
            dataList.append(dcV)
            dataList.append(dcA)
            dataList.append(alarm)
        
        
        
        index = 0

        for i in range(Monitoring.NUMBEROFDATA.value):
            # index 0:onoff 1:DCV 2:DCA 3:ALARM

            # 가동상태 라벨 on/off 색상 처리
            if dataList[index][0] is True:
                onoff = 'On'
                backgroundcolor = 'background-color:#84ff00;'
            else:
                onoff = 'Off'
                backgroundcolor = 'background-color:#ec2400;'

            self.statusLabelList[index].setStyleSheet(backgroundcolor)
            self.statusLabelList[index].setFont(QFont('맑은 고딕', 14))

            self.statusLabelList[index].setText(onoff)  
            # print(f"index is {index}")  
            index = index + 1
            for j in range(1, 3):
                
               
                self.statusLabelList[index].setFont(QFont('맑은 고딕', 14))   

                text = str(dataList[index])
                # 텍스트에 붙어 나오는 [ ] 제거
                text = text[1:len(text)-1]
                if j is 1:

                    # plc에서 받은 전압값 / 10 해줘야 정상 전압으로 표시
                    data = int(text)
                    data = data / 10
                    text = str(data)

                self.statusLabelList[index].setText(text)
                
                index = index +  1   
            # alarm 
            self.statusLabelList[index].setFont(QFont('맑은 고딕', 14))  
            self.statusLabelList[index].setText(str(dataList[index][0])) 
            index = index +  1   
            
            # print(f"index is {index}")    
                

            
            
    
    # 버튼의 이름을 통해 현장과 현장의 A,B,C호기를 판별함
    def setLocation(self, location):

        # 버튼 이름이 의정부_A 식으로 되어있음. _를 기준으로 접속 위치와 몇호기 인지를 판별할 수 있음.
        location = location.split("_")

        lo = location[0]
        machineStartReg = 0
        machineStartCoil = 0

        if len(location) == 1:
            machineStartReg = Machine.FIRSTREG.value
            machineStartCoil = Machine.FIRSTCOIL.value

        elif location[1] == 'A':
            machineStartReg = Machine.FIRSTREG.value
            machineStartCoil = Machine.FIRSTCOIL.value
        
        elif location[1] == 'B':
            machineStartReg = Machine.SECONDREG.value
            machineStartCoil = Machine.SECONDCOIL.value

        elif location[1] == 'C':
            machineStartReg = Machine.THIRDREG.value
            machineStartCoil = Machine.THRIDCOIL.value


        return lo, machineStartReg, machineStartCoil

    # 버튼 슬롯, 클릭한 버튼 판별을 위해 state, button 추가
    @pyqtSlot()
    def slotConnectButton(self, state, button):
        # 현장과 현장의 몇호기를 연결할 것인가를 버튼 이름을 통해 판별
        location, machineStartReg, machineStartCoil = self.setLocation(button.text())

        print(f"location {location} , machineStartCoil {machineStartCoil}, machineStartReg {machineStartReg}")
        self.mainWindow = MainWindow()
        self.mainWindow.connect(self.connectListDict[location])
        self.mainWindow.setStartCoilandReg(machineStartCoil, machineStartReg)
        self.mainWindow.show()

    def closeEvent(self, QCloseEvent):
        print("Enter CloseEvent")
        # self.plcConnect.closeClient()
        self.deleteLater()
        QCloseEvent.accept()


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    w = MonitoringWindow()
    w.show()
    sys.exit(app.exec())
   