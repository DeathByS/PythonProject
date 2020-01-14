# coding: utf-8

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QTabWidget
from PyQt5 import uic
from PyQt5 import QtGui
from PyQt5.QtGui import QFont
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtCore import QModelIndex
from PyQt5.QtCore import QTimer
from enums import Coils

import time

class MainWindowStatusTab(QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)   
        
        # MainWindow 폼의 위젯을 조작할 것이기 때문에 MainWindow를 parent로 받아 MainWindow의 위젯을 조작함
        self.parent = parent
        self.statusLabelList = []
        self.initWidget()

        self.timer = QTimer(self)
        self.timer.setInterval(3000)
        self.timer.start()
        self.timer.timeout.connect(self.changeStatus)
        
    def initWidget(self):
        self.statusLabelList.append(self.parent.label_status1)
        self.statusLabelList.append(self.parent.label_status2)
        self.statusLabelList.append(self.parent.label_status3)
        self.statusLabelList.append(self.parent.label_status4)
        self.statusLabelList.append(self.parent.label_status5)
        self.statusLabelList.append(self.parent.label_status6)
        self.statusLabelList.append(self.parent.label_status7)
        self.statusLabelList.append(self.parent.label_status8)
        self.statusLabelList.append(self.parent.label_status9)
        self.statusLabelList.append(self.parent.label_status10)
        self.statusLabelList.append(self.parent.label_status11)
        self.statusLabelList.append(self.parent.label_status12)
        self.statusLabelList.append(self.parent.label_status13)
        self.statusLabelList.append(self.parent.label_status14)
        self.statusLabelList.append(self.parent.label_status15)
        self.statusLabelList.append(self.parent.label_status16)
        
    def changeStatus(self):
    
        coils = self.parent.plcConnect.readCoil(0, 95)
        status = 'OFF'
        if coils == 'read error':
            self.timer.stop()
            print("read error, check Connect ")
            return "error"
             
        else:
          
        #  구동 준비
            if(coils[Coils.READY.value] == 0):
                backgroundcolor = 'background-color:#f0f0f0;'
            else:
                backgroundcolor = 'background-color:#84ff00;'

            self.statusLabelList[0].setStyleSheet(backgroundcolor)
            self.statusLabelList[0].setFont(QFont('맑은 고딕', 18))  

        # 현장 / 원격 모드
            if(coils[Coils.FIELDMODE.value] == 0):
                self.statusLabelList[1].setStyleSheet('background-color:#f0f0f0;')
                self.statusLabelList[1].setFont(QFont('맑은 고딕', 18))  
                self.statusLabelList[2].setStyleSheet('background-color:#84ff00;')
                self.statusLabelList[2].setFont(QFont('맑은 고딕', 18))     
            elif(coils[Coils.REMOTEMODE.value] == 0):
                self.statusLabelList[2].setStyleSheet('background-color:#f0f0f0;')
                self.statusLabelList[2].setFont(QFont('맑은 고딕', 18))  
                self.statusLabelList[1].setStyleSheet('background-color:#84ff00;')
                self.statusLabelList[1].setFont(QFont('맑은 고딕', 18))     
        
        # 수동 / 자동조작
            if(coils[Coils.MANUAL.value] == 0):
                self.statusLabelList[3].setStyleSheet('background-color:#f0f0f0;')
                self.statusLabelList[3].setFont(QFont('맑은 고딕', 18))  
                self.statusLabelList[4].setStyleSheet('background-color:#84ff00;')
                self.statusLabelList[4].setFont(QFont('맑은 고딕', 18))     
            elif(coils[Coils.AUTO.value] == 0):
                self.statusLabelList[4].setStyleSheet('background-color:#f0f0f0;')
                self.statusLabelList[4].setFont(QFont('맑은 고딕', 18))  
                self.statusLabelList[3].setStyleSheet('background-color:#84ff00;')
                self.statusLabelList[3].setFont(QFont('맑은 고딕', 18))     
        # 자동 시작 / 자동 멈춤
            if(coils[Coils.AUTOMATICSTART.value] == 0):
                self.statusLabelList[5].setStyleSheet('background-color:#f0f0f0;')
                self.statusLabelList[5].setFont(QFont('맑은 고딕', 18))  
                self.statusLabelList[6].setStyleSheet('background-color:#84ff00;')
                self.statusLabelList[6].setFont(QFont('맑은 고딕', 18))     
            elif(coils[Coils.AUTOMATICSTOP.value] == 0):
                self.statusLabelList[6].setStyleSheet('background-color:#f0f0f0;')
                self.statusLabelList[6].setFont(QFont('맑은 고딕', 18))  
                self.statusLabelList[5].setStyleSheet('background-color:#84ff00;')
                self.statusLabelList[5].setFont(QFont('맑은 고딕', 18))     

            labelListIndex = 7
            for i in range(Coils.CAMMOTER.value, Coils.SLIPRINGCOLLINGFAN.value + 1):
                if coils[i] == 0:
                    status = 'OFF'
                    backgroundcolor = 'background-color:#ec2400;'

                else:
                    status = 'ON'
                    backgroundcolor = 'background-color:#84ff00;'
                
                self.statusLabelList[labelListIndex].setText(status)
                self.statusLabelList[labelListIndex].setStyleSheet(backgroundcolor)
                self.statusLabelList[labelListIndex].setFont(QFont('맑은 고딕', 18))
                print(labelListIndex)
                labelListIndex = labelListIndex + 1 
           

            
               

              




        