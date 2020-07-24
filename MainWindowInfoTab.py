# coding: utf-8

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QTabWidget
from PyQt5 import uic
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtCore import QModelIndex
from PyQt5.QtCore import QTimer
from enums import Regs, Machine
import time

class MainWindowInfoTab(QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)   
        print('init MainWindowInfoTab')
        # MainWindow 폼의 위젯을 조작할 것이기 때문에 MainWindow를 parent로 받아 MainWindow의 위젯을 조작함
        self.parent = parent
        self.lcdList = []
        self.numberOfAlarm = 0
        self.numberOfAbnormalSignAlarm = 0
        self.numberOfSludgeOutAlarm = 0
        self.numberOfPartChangeAlarm = 0

        self.initWidget()

        self.timer = QTimer(self)
        self.timer.setInterval(1000 * 10)
        self.timer.start()
        self.timer.timeout.connect(self.changelcdData)

    
        
    def initWidget(self):
        
        # 주파수, 온도 lcd
        self.lcdList.append(self.parent.lcdData_1)
        self.lcdList.append(self.parent.lcdData_2)
        self.lcdList.append(self.parent.lcdData_3)
        self.lcdList.append(self.parent.lcdData_4)
        self.lcdList.append(self.parent.lcdData_5)
        self.lcdList.append(self.parent.lcdData_6)
        self.lcdList.append(self.parent.lcdData_7)
        self.lcdList.append(self.parent.lcdData_8)

        #전압, 전력 lcd
        self.lcdList.append(self.parent.lcdData_9)
        self.lcdList.append(self.parent.lcdData_10)
        self.lcdList.append(self.parent.lcdData_11)
        self.lcdList.append(self.parent.lcdData_12)

        # 사행회수, 슬러지 배출, 소모품 교체, 알람, 이상
        self.lcdList.append(self.parent.lcdData_13)
        self.lcdList.append(self.parent.lcdData_14)
        self.lcdList.append(self.parent.lcdData_15)
        self.lcdList.append(self.parent.lcdData_16)
        self.lcdList.append(self.parent.lcdData_17)
        self.lcdList.append(self.parent.lcdData_18)

        
    def changelcdData(self):
        
        try:
            regs = self.parent.plcConnect.readRegister(self.parent.machineStartReg + Regs.DRUMFRQ.value, 
                                                        Regs.SLIPRINGTEMP.value + 1)

            #regs 10, 11번 = 슬러지 투입 / 배출량 Kg 단위에서 Ton 단위로 변환
            regs[Regs.INPUT.value] = regs[Regs.INPUT.value] / 10
            regs[Regs.OUTPUT.value] = regs[Regs.OUTPUT.value] / 10
            # 전압 값을 소수점 단위로 나타내기 위해 
            regs[Regs.DCV.value] = regs[Regs.DCV.value] / 10

            # 현장 데이터에서 / 10 해줘야 정상 데이터로 표시됨
            regs[Regs.DRUMFRQ.value] = regs[Regs.DRUMFRQ.value] / 10
            regs[Regs.PRESSROLLFRQ.value] = regs[Regs.PRESSROLLFRQ.value] / 10
            regs[Regs.SLUDEGSUPPLYFRQ.value] = regs[Regs.SLUDEGSUPPLYFRQ.value] / 10
            regs[Regs.SLUDEGSPREADFRQ.value] = regs[Regs.SLUDEGSPREADFRQ.value] / 10
            regs[Regs.DRUMCOLLINGWATER.value] = regs[Regs.DRUMCOLLINGWATER.value] / 10
            regs[Regs.TRANSFORMERSTEMP.value] = regs[Regs.TRANSFORMERSTEMP.value] / 10
            

        except:
            return
        
        # colis2, regs2 = self.parent.plcConnect2.readRegister()
        print(regs)
        if regs == 'read error':
            self.timer.stop()
            print("read error, check Connect ")
            return "error"
             
        else:
            # 주파수, 온도 lcd    
            self.lcdList[0].display(float(regs[Regs.DRUMFRQ.value]))
            self.lcdList[1].display(float(regs[Regs.PRESSROLLFRQ.value]))
            self.lcdList[2].display(float(regs[Regs.SLUDEGSUPPLYFRQ.value]))
            self.lcdList[3].display(float(regs[Regs.SLUDEGSPREADFRQ.value]))
            self.lcdList[4].display(float(regs[Regs.TRANSFORMERSTEMP.value]))
            self.lcdList[5].display(float(regs[Regs.SCRTEMP.value]))
            self.lcdList[6].display(float(regs[Regs.DRUMCOLLINGWATER.value]))
            self.lcdList[7].display(float(regs[Regs.SLIPRINGTEMP.value]))

            #전압, 전력 lcd
            self.lcdList[8].display(float(regs[Regs.DCV.value]))
            self.lcdList[9].display(float(regs[Regs.DCA.value]))
            self.lcdList[10].display(float(regs[Regs.CAPACITY.value]))
            self.lcdList[11].display(float(regs[Regs.DCV.value] * regs[Regs.DCA.value] / 1000))

            # 사행회수, 슬러지 배출, 소모품 교체, 알람, 이상
            self.lcdList[12].display(float(regs[Regs.LEFTBALANCE.value]))
            self.lcdList[13].display(float(regs[Regs.RIGHTBALANCE.value]))
            self.lcdList[14].display(float(self.numberOfAlarm))
            self.lcdList[15].display(float(self.numberOfSludgeOutAlarm))
            self.lcdList[16].display(float(self.numberOfPartChangeAlarm))
            self.lcdList[17].display(float(self.numberOfAbnormalSignAlarm))
            

           


              




        