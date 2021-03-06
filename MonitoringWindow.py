# coding: utf-8
 
import sys
import os
import csv
# import image_rc

from PyQt5 import QtWidgets, QtGui
from PyQt5 import uic
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtCore import QModelIndex
from sync_Client import SyncClient 
from PyQt5.QtGui import QFont
from PyQt5.QtCore import QTimer
from enums import Coils, Machine, Regs, Monitoring, OptimizerData, WriteValue
from MainWindowOperatingTimeTab import MainWindowOperatingTimeTab
from MainWindow import MainWindow
from datetime import datetime
import time


class MonitoringWindow(QtWidgets.QMainWindow):
    
    def __init__(self):
        super().__init__()
       
        # path = os.path.abspath('MonitoringForm.ui')
        
        print(os.getcwd())
        uic.loadUi(os.getcwd()+"\MonitoringForm.ui", self)

        # 연결 위치 : key, Plc Connection Object : Value
        self.plcConnectDict = {} 
        self.plcConnect = 0
        self.ip = None

        self.dataCount = 0
        self.receiveTime = []
        self.receiveData = []
        
        self.statusLabelList = []
        self.locationButtonList = []

        self.connectListDict = {}

        self.connectList = []

        self.initConnectionList()
        self.initStatusLabel()
        self.initLocationButton()

        self.initPlcConnect()

        self.changeStatusLabel()

        self.timer = QTimer(self) 
        self.timer.setInterval(10000)
        self.timer.start()
        self.timer.timeout.connect(self.changeStatusLabel)

        self.timer2 = QTimer(self)
        # 30분 정도에 한번씩 운전상황 업데이트 시간 체크하여 새벽 12시 이후에 운전상황 업데이트
        self.timer2.setInterval(1000 * 60 * 60)
        self.timer2.start()
        self.timer2.timeout.connect(self.optimizeStatus)
        # self.setFocusPolicy(Qt.Qt.Strong)

        # 하트비트 핑 패킷 체크용
        # self.timer3 = QTimer(self)
        # self.timer3.setInterval(1000 * 10  * 1)
        # self.timer3.start()
        # self.timer3.timeout.connect(self.pingPrint)

   
        

    def initConnectionList(self):
        print(os.getcwd())
        with open("data/ConnectionList.csv", 'r', encoding='utf-8') as f:
            rdr = csv.reader(f)
            
            connList = [] 
            
            for row in rdr:
                self.connectList.append(row[0])
                #  print(connList)
                #  self.connectListBox.addItem(row[0])

            # self.connectListDict = dict(self.connectList)
            print(self.connectList)

    def initPlcConnect(self):
            # 딕셔너리의 키만 받아서 리스트 같이 사용
        # for i in self.connectListDict.keys():
        #     try:
        #         self.plcConnectDict[i] = (self.connect(self.connectListDict[i]))
        #         print('plcConnectDict[i] = ', self.plcConnectDict[i])
        #     except:
            
        #         self.plcConnectDict[i] = False
        #         print('plcConnectDict[i] = ', self.plcConnectDict[i])
        self.plcConnect = self.connect()



    def initStatusLabel(self):
        
        for i in range(1, Monitoring.NUMBEROFLABELS.value + 1):
            # 오브젝트의 이름을 가지고 오브젝트 찾아 사용하는법.
            labelName = "label_%d" % i
            # print(labelName)
            self.statusLabelList.append(self.findChild(QtWidgets.QLabel, labelName))

    
                

    def initLocationButton(self):
        for i in range(1, Monitoring.NUMBEROFBUTTONS.value + 1):
            # 오브젝트의 이름을 가지고 오브젝트 찾아 사용하는법.
            buttonName = "pushButton_%d" % i
            self.locationButtonList.append(self.findChild(QtWidgets.QPushButton, buttonName))

        for i in self.locationButtonList:
            i.clicked.connect(lambda state, button=i : self.slotConnectButton(state, button))


    def connect(self, ip = 'kwtkorea.iptime.org'):
        plcConnect = SyncClient()
        if plcConnect.connectClient(ip, 502):
            print(plcConnect)
            return plcConnect
        else:
            print('connect error')
            return False

        

    def changeStatusLabel(self):
        # print("changes %d"%len(self.locationButtonList))
        
        dataList = []
        connectList = self.connectListDict.keys()
        afterLocation = ''

        # for j in range(len(self.locationButtonList)):
        for i in self.connectList:  
            
            location, machineStartReg, machineStartCoil = self.setLocation(i)

            print(location, machineStartCoil, machineStartReg)
            
            # 일단 연결이 안된걸 확인, 재연결 시도 후 연결 안되면 모든 데이터에 0을 삽입
            
            # if(self.plcConnectDict[location] == False):
            #     if(self.connectListDict[location] != afterLocation):
            #         print('c연결시도')
            #         print(self.plcConnectDict[location])
            #         print(self.connectListDict)
            #         self.plcConnectDict[location] = (self.connect(self.connectListDict[location]))
            #         afterLocation = self.connectListDict[location]



            try:    
                onoff = self.plcConnect.readCoil(machineStartCoil + Coils.AUTOMATICSTART.value, 1)
                # print(onoff)
                dcV = self.plcConnect.readRegister(machineStartReg + Regs.DCV.value, 1)
                if(location == '검단_A' or location == '검단_B'):
                    dcV[0] = dcV[0] * 10
                dcA = self.plcConnect.readRegister(machineStartReg + Regs.DCA.value, 1)
                alarm = self.plcConnect.readCoil(machineStartCoil + Coils.REMOTESTOP.value, 1)
                
                # dcA의 쓰레기값 처리
                if(dcA[0] > 65000):
                    dcA[0] = 0     
            except:
                print('error Changelabel')
                onoff = [0]
                dcV = [0]
                dcA = [0]
                alarm = [0]
                
          
            
            dataList.append(onoff)
            dataList.append(dcV)
            dataList.append(dcA)
            dataList.append(alarm)

        print(dataList)
        
        index = 0
        
        for i in range(Monitoring.NUMBEROFDATA.value):
            # index 0:onoff 1:DCV 2:DCA 3:ALARM

            # 가동상태 라벨 on/off 색상 처리
            try:
                if dataList[index][0] is True:
                    onoff = 'On'
                    backgroundcolor = 'color:#00e600;'
                else:
                    onoff = 'Off'
                    backgroundcolor = 'color:#ec2400;'
            
            except:
                print('bool object error')
                pass

            # print('index %d'%index)
            self.statusLabelList[index].setStyleSheet('background-image: url(:/image/label4.png); ' + backgroundcolor)
            self.statusLabelList[index].setFont(QFont('맑은 고딕', 14))

            self.statusLabelList[index].setText(onoff)  
            # print(f"index is {index}")  
            index = index + 1
            for j in range(1, 3):
                
               
                self.statusLabelList[index].setFont(QFont('맑은 고딕', 14))   

                text = str(dataList[index])
                # 텍스트에 붙어 나오는 [ ] 제거
                text = text[1:len(text)-1]
                if (j == 1):

                    # plc에서 받은 전압값 / 10 해줘야 정상 전압으로 표시
                    data = int(text)
                    
                    data = data / 10
                    text = str(data)

                self.statusLabelList[index].setText(text)
                
                index = index +  1   
            # alarm 
            self.statusLabelList[index].setFont(QFont('맑은 고딕', 14)) 

            try:
                self.statusLabelList[index].setText(str(dataList[index][0])) 
                index = index +  1   
            except:
                print('bool object error')
                pass
            # print(f"index is {index}")    
                
            
        # self.optimizeStatus()     
            
    
    # 버튼의 이름을 통해 현장과 현장의 A,B,C호기를 판별함
    def setLocation(self, location):

        # 버튼 이름이 의정부_A 식으로 되어있음. _를 기준으로 접속 위치와 몇호기 인지를 판별할 수 있음.
        # location = location.split("_")

        # lo = location[0]

        
        machineStartReg = 0
        machineStartCoil = 0

        index = self.connectList.index(location)

        machineStartReg = Machine.TERMOFREG.value * index
        machineStartCoil = Machine.TERMOFCOIL.value * index

        # # 기계 대수가 1대라서 a,b,c 구분이 없고 오직 이름으로만 구성되어있을때 ex)서울
        # if len(location) == 1: 
        #     machineStartReg = Machine.FIRSTREG.value
        #     machineStartCoil = Machine.FIRSTCOIL.value
        # # A호기 ex)의정부_A
        # elif location[1] == 'A':
        #     machineStartReg = Machine.FIRSTREG.value
        #     machineStartCoil = Machine.FIRSTCOIL.value
        
        # elif location[1] == 'B':
        #     machineStartReg = Machine.SECONDREG.value
        #     machineStartCoil = Machine.SECONDCOIL.value

        # elif location[1] == 'C':
        #     machineStartReg = Machine.THIRDREG.value
        #     machineStartCoil = Machine.THRIDCOIL.value


        return location, machineStartReg, machineStartCoil

    # 버튼 슬롯, 클릭한 버튼 판별을 위해 state, button 추가
    @pyqtSlot()
    def slotConnectButton(self, state, button):
        # 현장과 현장의 몇호기를 연결할 것인가를 버튼 이름을 통해 판별
        location, machineStartReg, machineStartCoil = self.setLocation(button.text())

        # print(f"location {location} , machineStartCoil {machineStartCoil}, machineStartReg {machineStartReg}")

        self.mainWindow = MainWindow(button.text(), self.plcConnect, machineStartReg, machineStartCoil)
        # self.mainWindow.connect(self.connectListDict[location])
        # self.mainWindow.setStartCoilandReg(machineStartCoil, machineStartReg)
        # self.mainWindow.setMachineName()
        self.mainWindow.show()

    def closeEvent(self, QCloseEvent):
        print("Enter CloseEvent")
        # self.plcConnect.closeClient()
        self.deleteLater()
        QCloseEvent.accept()


    def optimizeStatus(self):
        # 정해진 시간에 맞춰 운전 조건을 업데이트 해주는 기능.
        for i in range(len(self.locationButtonList)): 
            
            location, machineStartReg, machineStartCoil = self.setLocation(self.locationButtonList[i].text())

            # plc의 시간을 가져와서 쓴다. 시작번지 500  # 시간 = 초 분 시 일 월 순
            # time = self.plcConnectDict[location].readRegister(machineStartReg + 500,5)
            # print('time ' + self.locationButtonList[i].text())
            # print(time)
            
            # 새벽 12시 기준으로 운전상황을 업데이트 할것이다.
            # 테스트 중에는 1시간에 1번으로.
            # if(time[2] != 0):
            #     return
            
            # 알고리즘 계산시 사용할 변수들 시작번지 3000
            optimizeData = self.plcConnect.readRegister(OptimizerData.AVGINPUTWATERRATE.value, 13)
            # print('time ' + self.locationButtonList[i].text())
            print("optimizeData", optimizeData)
            
            # 알고리즘 식을 통해 조정값 산출

            # try:
                # 3000 = 시작번지
            dcV =   (
                    ((1 - (1 - optimizeData[OptimizerData.BASEINPUTWATERRATE.value - 3000]/1000) / (1 - optimizeData[OptimizerData.BASEOUTPUTWATERRATE.value- 3000]/1000))/ 
                    (1 - (1 - optimizeData[OptimizerData.AVGINPUTWATERRATE.value- 3000] /1000) / (1 - optimizeData[OptimizerData.AVGOUTPUTWATERRATE.value- 3000] /1000)))*
                    (optimizeData[OptimizerData.AVGSLUDGEINPUT.value- 3000]/ optimizeData[OptimizerData.BASESLUDGEINPUT.value- 3000]) * optimizeData[OptimizerData.BASEDCV.value- 3000]
                    )

            drumFrq = optimizeData[OptimizerData.BASEDRUMFRQ.value- 3000] *  (optimizeData[OptimizerData.AVGSLUDGEINPUT.value- 3000]
            / optimizeData[OptimizerData.BASESLUDGEINPUT.value- 3000])

            pusherFrq = optimizeData[OptimizerData.BASEPUSSERFRQ.value- 3000] * (drumFrq / optimizeData[OptimizerData.BASEDRUMFRQ.value- 3000])        

            print('Optimize Data dcV %f DrumFrq %f pusherFrq %f'%(dcV, drumFrq, pusherFrq))

            data = []
            data.append(int(dcV))
            data.append(int(drumFrq))   
            data.append(int(pusherFrq))

            starttime = datetime.now()
            self.plcConnect.writeRegisters(WriteValue.VOLTAGE.value, data)

            with open("log/OptimizeStatusChangeLog.txt", "a", encoding='utf-8') as f:    
                f.write(str(starttime) + ' %s 운전 조건 변경 전압 %d 드럼속도 %d 푸셔속도 %d\n'%(self.locationButtonList[i].text()
                ,int(dcV), int(drumFrq), int(pusherFrq)))

            # except:
            #     print('Error')
            #     return 'error'

    # def resultPrint(self):
    #     # print('%d 개의 데이터를 받음'%self.dataCount)
    #     # print('성공 : %d, 실패 %d'%(self.receiveData.count(44770), self.receiveData.count(False)))
    #     # print('Min = %.3fms, Max = %.3fms, Avg = %.3fms'%(min(self.receiveTime),max(self.receiveTime),
    #     #  sum(self.receiveTime) / len(self.receiveTime)))

    #     with open("log/PingTestLog.txt", "at") as f:
    #         f.write('%d 개의 데이터를 받음\n'%self.dataCount)
    #         f.write('성공 : %d, 실패 %d\n'%(self.receiveData.count(True), self.receiveData.count(False)))
    #         f.write('Min = %.3fms, Max = %.3fms, Avg = %.3fms\n'%(min(self.receiveTime),max(self.receiveTime),
    #          sum(self.receiveTime) / len(self.receiveTime)))

    # def pingPrint(self):
    #     try:
    #         location = 'kwtkorea.iptime.org'
    #         plc = SyncClient()
    #         if(plc.connectClient(location)):
    #             data = 0
    #             self.dataCount += 1
    #             beforeTime = datetime.now()
    #             beforeTime2 = time.time()
    #             print(str(beforeTime) + ' connect %s'%location)
    #             # 44770
    #             data = plc.readRegister(4900,10)
    #             plc.closeClient()
    #             afterTime = datetime.now()
    #             afterTime2 = time.time()
    #             # print('pingdata ', data[0])
    #             runTime = round((afterTime2 - beforeTime2) * 1000, 5)

    #             with open("log/PingTestLog.txt", "at", encoding='utf-8') as f:
    #                 f.write(str(beforeTime) + ' connect %s\n'%location)
    #                 f.write(str(runTime)+'ms\n')


    #             self.receiveTime.append(runTime)
    #             self.receiveData.append(True)
    #             # print('ping ok')

    #         else: 
    #             self.dataCount += 1
    #             # print('ping false')
    #             self.receiveData.append(False) 

    #         self.resultPrint()     
    #     except:
    #         self.resultPrint()      


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    w = MonitoringWindow()
    # w.optimizeStatus()
    w.show()
    sys.exit(app.exec())
   