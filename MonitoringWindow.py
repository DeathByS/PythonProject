# coding: utf-8
 
import sys
import csv

from PyQt5 import QtWidgets
from PyQt5 import uic
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtCore import QModelIndex
from sync_Client import SyncClient 
from PyQt5.QtGui import QFont
from PyQt5.QtCore import QTimer
from enums import Coils, Machine, Regs
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
        self.label_1.setText("AAA")

        self.connectListDict = {}
        self.initConnectionList()
        self.initStatusLabel()
        self.initLocationButton()

        self.initPlcConnect()

        self.changeStatusLabel()

        
        

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
        self.statusLabelList.append(self.label_1)
        self.statusLabelList.append(self.label_2)
        self.statusLabelList.append(self.label_3)
        self.statusLabelList.append(self.label_4)
        self.statusLabelList.append(self.label_5)
        self.statusLabelList.append(self.label_6)
        self.statusLabelList.append(self.label_7)
        self.statusLabelList.append(self.label_8)
        self.statusLabelList.append(self.label_9)
        self.statusLabelList.append(self.label_10)
        self.statusLabelList.append(self.label_11)
        self.statusLabelList.append(self.label_12)
        self.statusLabelList.append(self.label_13)
        self.statusLabelList.append(self.label_14)
        self.statusLabelList.append(self.label_15)
        self.statusLabelList.append(self.label_16)


    def initLocationButton(self):
        self.locationButtonList.append(self.pushButton_1)
        self.locationButtonList.append(self.pushButton_2) 
        self.locationButtonList.append(self.pushButton_3) 
        self.locationButtonList.append(self.pushButton_4) 

        for i in self.locationButtonList:
            i.clicked.connect(lambda state, button=i : self.slotConnectButton(state, button))


    def connect(self, ip = "kwtkorea.iptime.org"):
        plcConnect = SyncClient()
        plcConnect.connectClient(ip, 502)
        return plcConnect

    def changeStatusLabel(self):
        print("changes")
        

        dataList = []


        
        for j in range(0, 4): 
            # print(f"index is {index}")
            location, machineStartReg, machineStartCoil = self.setLocation(self.locationButtonList[j].text())
            onoff = self.plcConnectDict[location].readCoil(machineStartCoil + Coils.AUTOMATICSTART.value, 1)
            dcV = self.plcConnectDict[location].readRegister(machineStartReg + Regs.DCV.value, 1)
            dcA = self.plcConnectDict[location].readRegister(machineStartReg + Regs.DCA.value, 1)
            alarm = self.plcConnectDict[location].readCoil(machineStartCoil + Coils.REMOTESTOP.value, 1)

            dataList.append(onoff)
            dataList.append(dcV)
            dataList.append(dcA)
            dataList.append(alarm)
        
        print(f"dataList is {dataList}")
        
        index = 0

        for i in range(0, 4):

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
                
                print(f"index is {index}")
                self.statusLabelList[index].setFont(QFont('맑은 고딕', 14))   

                text = str(dataList[index])
                text = text[1:len(text)-1]
                if j is 1:
                    data = int(text)
                    data = data / 10
                    text = str(data)

                self.statusLabelList[index].setText(text)
                
                index = index +  1   

            self.statusLabelList[index].setFont(QFont('맑은 고딕', 14))  
            self.statusLabelList[index].setText(str(dataList[index][0])) 
            index = index +  1   
            
            # print(f"index is {index}")    
                

            
            
    
    # 버튼의 이름을 통해 현장과 현장의 A,B,C호기를 판별함
    def setLocation(self, location):

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
   