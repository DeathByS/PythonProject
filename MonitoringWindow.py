# coding: utf-8
 
import sys
import csv
import image_rc

from PyQt5 import QtWidgets, QtGui
from PyQt5 import uic
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtCore import QModelIndex
from sync_Client import SyncClient 
from PyQt5.QtGui import QFont
from PyQt5.QtCore import QTimer
from enums import Coils, Machine, Regs, Monitoring, OptimizerData
from MainWindow import MainWindow
from datetime import datetime
 
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

        self.timer2 = QTimer(self)
        # 30분 정도에 한번씩 운전상황 업데이트 시간 체크하여 새벽 12시 이후에 운전상황 업데이트
        self.timer2.setInterval(1000 * 60  * 30)
        self.timer2.start()
        self.timer2.timeout.connect(self.optimizeStatus)
        # self.setFocusPolicy(Qt.Qt.Strong)

        
        

    def initConnectionList(self):
    
        with open('data/ConnectionList.csv', 'r', encoding='utf-8') as f:
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
            try:
                self.plcConnectDict[i] = (self.connect(self.connectListDict[i]))
            except:
                self.plcConnectDict[i] = False


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
        # print("changes")
        

        dataList = []


        
        for j in range(len(self.locationButtonList)): 
            
            location, machineStartReg, machineStartCoil = self.setLocation(self.locationButtonList[j].text())
            
            # 일단 연결이 안된걸 확인, 재연결 시도 후 연결 안되면 모든 데이터에 0을 삽입
            try:
                # if(self.plcConnectDict[location] == False):
                #     print('c연결시도')
                #     self.plcConnectDict[location] = (self.connect(self.connectListDict[j])) 

                
                onoff = self.plcConnectDict[location].readCoil(machineStartCoil + Coils.AUTOMATICSTART.value, 1)
                dcV = self.plcConnectDict[location].readRegister(machineStartReg + Regs.DCV.value, 1)
                dcA = self.plcConnectDict[location].readRegister(machineStartReg + Regs.DCA.value, 1)
                alarm = self.plcConnectDict[location].readCoil(machineStartCoil + Coils.REMOTESTOP.value, 1)
                
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
        
        
        
        index = 0

        for i in range(Monitoring.NUMBEROFDATA.value):
            # index 0:onoff 1:DCV 2:DCA 3:ALARM

            # 가동상태 라벨 on/off 색상 처리
            if dataList[index][0] is True:
                onoff = 'On'
                backgroundcolor = 'color:#00e600;'
            else:
                onoff = 'Off'
                backgroundcolor = 'color:#ec2400;'

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
            self.statusLabelList[index].setText(str(dataList[index][0])) 
            index = index +  1   
            
            # print(f"index is {index}")    
                
            
        # self.optimizeStatus()     
            
    
    # 버튼의 이름을 통해 현장과 현장의 A,B,C호기를 판별함
    def setLocation(self, location):

        # 버튼 이름이 의정부_A 식으로 되어있음. _를 기준으로 접속 위치와 몇호기 인지를 판별할 수 있음.
        location = location.split("_")

        lo = location[0]
        machineStartReg = 0
        machineStartCoil = 0

        # 기계 대수가 1대라서 a,b,c 구분이 없고 오직 이름으로만 구성되어있을때 ex)서울
        if len(location) == 1: 
            machineStartReg = Machine.FIRSTREG.value
            machineStartCoil = Machine.FIRSTCOIL.value
        # A호기 ex)의정부_A
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

        # print(f"location {location} , machineStartCoil {machineStartCoil}, machineStartReg {machineStartReg}")

        self.mainWindow = MainWindow(button.text(), self.connectListDict[location], machineStartReg, machineStartCoil)
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
            time = self.plcConnectDict[location].readRegister(machineStartReg + 500,5)
            # print('time ' + self.locationButtonList[i].text())
            print(time)
            
            # 새벽 12시 기준으로 운전상황을 업데이트 할것이다.
            if(time[2] != 0):
                return
            
            # 알고리즘 계산시 사용할 변수들 시작번지 1400
            optimizeData = self.plcConnectDict[location].readRegister(machineStartReg + 1400, 13)
            # print('time ' + self.locationButtonList[i].text())
            print(optimizeData)
            
            # 알고리즘 식을 통해 조정값 산출

            try:
                dcV =   (
                        ((1 - (1 - optimizeData[OptimizerData.BASEINPUTWATERRATE.value]/100) / (1 - optimizeData[OptimizerData.BASEOUTPUTWATERRATE.value]/100))/ 
                        (1 - (1 - optimizeData[OptimizerData.AVGINPUTWATERRATE.value] /100) / (1 - optimizeData[OptimizerData.AVGOUTPUTWATERRATE.value] /100)))*
                        (optimizeData[OptimizerData.AVGSLUDGEINPUT.value]/ optimizeData[OptimizerData.BASESLUDGEINPUT.value]) * optimizeData[OptimizerData.BASEDCV.value]
                        )

                drumFrq = optimizeData[OptimizerData.BASEDRUMFRQ.value] *  (optimizeData[OptimizerData.AVGSLUDGEINPUT.value]/ optimizeData[OptimizerData.BASESLUDGEINPUT.value])

                pusherFrq = optimizeData[OptimizerData.BASEPUSSERFRQ.value] * (drumFrq / optimizeData[OptimizerData.BASEDRUMFRQ.value])        

                print('Optimize Data dcV %f DrumFrq %f pusherFrq %f'%(dcV, drumFrq, pusherFrq))

                data = []
                data.append(int(dcV))
                data.append(int(drumFrq))
                data.append(int(pusherFrq))

                starttime = datetime.now()
                self.plcConnectDict[location].writeRegisters(machineStartReg + 250, data)

                with open("log/OptimizeStatusChangeLog.txt", "a", encoding='utf-8') as f:    
                    f.write(str(starttime) + ' %s 운전 조건 변경 전압 %d 드럼속도 %d 푸셔속도 %d'%(self.locationButtonList[i].text()
                    ,int(dcV), int(drumFrq), int(pusherFrq)))

            except:
                # print('zero division Error')
                return 'error'

           


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    w = MonitoringWindow()
    w.show()
    sys.exit(app.exec())
   