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
from enums import Coils, Machine
from SingletonInstance import GetDataFromDB
import datetime

class MainWindowStatusTab(QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)   
        
        # MainWindow 폼의 위젯을 조작할 것이기 때문에 MainWindow를 parent로 받아 MainWindow의 위젯을 조작함
        self.parent = parent
        self.statusLabelList = []
        self.initWidget()

        self.timer = QTimer(self)
        self.timer.setInterval(5000)
        self.timer.start()
        self.timer.timeout.connect(self.changeStatus)
        
        
    def initWidget(self):
        #슬러지 투입 관련 라벨
        self.statusLabelList.append(self.parent.lcd_status_1)
        self.statusLabelList.append(self.parent.lcd_status_2)
        self.statusLabelList.append(self.parent.lcd_status_3)
        self.statusLabelList.append(self.parent.lcd_status_4)

        # 함수율 관련 라벨
        self.statusLabelList.append(self.parent.lcd_status_5)
        self.statusLabelList.append(self.parent.lcd_status_6)
        self.statusLabelList.append(self.parent.lcd_status_7)
        self.statusLabelList.append(self.parent.lcd_status_8)

        # 슬러지 배출량 관련 라벨
        self.statusLabelList.append(self.parent.lcd_status_9)
        self.statusLabelList.append(self.parent.lcd_status_10)
        self.statusLabelList.append(self.parent.lcd_status_11)
        self.statusLabelList.append(self.parent.lcd_status_12)

        # 전력량 관련 라벨
        self.statusLabelList.append(self.parent.lcd_status_13)
        self.statusLabelList.append(self.parent.lcd_status_14)

        
    def changeStatus(self):
        
        # 총 투입량 계산용
        totalSludgeInput = 0.0
        totalSludgeOutput = 0.0

        # 누적 전력량 계산용
        totalKW = 0.0

        #평균 함수율 계산용
        totalInputWaterRate = 0.0
        totalOutputWaterRate = 0.0
        
        # 평균 시간당 투입량 계산 시 투입량이 0인 구간 제거용 
        totalZeroInputSection = 0
        totalZeroOutputSection = 0  

        # 평균 함수율에서 함수율이 0인 곳 제거용

        totalZeroInputWaterRate = 0
        totalZeroOutputWaterRate = 0
        
        # 시간당 투입량 계샨용
        sludgeInputPerHour = 0
        sludgeOutputPerHour = 0


        # 시간당 투입량 / 배출량 / 투입, 배출 함수율
        getData = GetDataFromDB.instance()
        
        current = datetime.datetime.now()
        oneHourago = current - datetime.timedelta(hours=1)

        # tableName, machineName, colName ,start, end
        
        try:
            data = getData.getDataInRange('InfoData','timeData', str(oneHourago), str(current),self.parent.machineName)

        except:
            return 'error'
        

        for i in data:
            sludgeInputPerHour = sludgeInputPerHour + i['sludgeInput']
            sludgeOutputPerHour = sludgeOutputPerHour + i['sludgeOutput']

        #슬러지가 kg 단위기 때문에 톤으로 변환
        sludgeInputPerHour = sludgeInputPerHour / 1000 
        sludgeOutputPerHour = sludgeOutputPerHour / 1000    
        self.statusLabelList[0].display(sludgeInputPerHour)
        self.statusLabelList[8].display(sludgeOutputPerHour)

        # 투입 / 배출 함수율 (아직 함수율 측정기가 완성되지 않았으므로 설정된 값으로..)

        inputWaterRate = data[len(data)-1]['inputwaterRate'] 
        outputWaterRate = data[len(data)-1]['outputwaterRate']
        self.statusLabelList[4].display(inputWaterRate)
        self.statusLabelList[6].display(outputWaterRate)
        
        # 누적 투입량 /배출량 / 누적 전력량

        current = datetime.datetime.now()
        ago = current - datetime.timedelta(days=int(self.parent.inputDay.text()))

        

        # tableName, machineName, colName ,start, end
        
        try:
            data = getData.getDataInRange('InfoData','timeData', str(ago), str(current),self.parent.machineName)

        except:
            return 'error'

        for i in data:
            totalSludgeInput = totalSludgeInput + i['sludgeInput']
            totalSludgeOutput = totalSludgeOutput + i['sludgeOutput']

            totalInputWaterRate = totalInputWaterRate + i['inputwaterRate']
            totalOutputWaterRate = totalOutputWaterRate + i['outputwaterRate']
            
            totalKW = totalKW + i['kW']


            # 슬러지 투입/배출 중 0인 부분은 제외하기 위해 0인 부분의 개수를 체크한다 (시간당 투입율 계산용)
            if(i['sludgeInput'] == 0):
                totalZeroInputSection = totalZeroInputSection + 1

            if(i['sludgeOutput'] == 0):    
                totalZeroOutputSection = totalZeroOutputSection + 1


            #함수율이 0인 구간을 제외하기 위하여 개수 체크(평균 투입/배출함수율 계산용)

            if(i['inputwaterRate'] == 0):
                totalZeroInputWaterRate = totalZeroInputWaterRate + 1

            if(i['outputwaterRate'] == 0):    
                totalZeroOutputWaterRate = totalZeroOutputWaterRate + 1

            

        totalSludgeInput = totalSludgeInput / 1000
        totalSludgeOutput = totalSludgeOutput / 1000
        totalKW = totalKW / 1000

        try:
            self.statusLabelList[3].display(totalSludgeInput) 
            self.statusLabelList[11].display(totalSludgeOutput)    
            self.statusLabelList[12].display(totalKW)
            self.statusLabelList[13].display(totalSludgeInput / totalKW)
        except:
            pass


        # 평균 시간당 투입량 /배출량,  평균 투입 /배출 함수율

        totalInputWorkTime = (len(data) - totalZeroInputSection) / 6 
        totalOutputWorkTime = (len(data) - totalZeroOutputSection) / 6

        try:
            averageSludgeInputPerHour = totalSludgeInput / totalInputWorkTime
            averageSludgeOutputPerHour = totalSludgeOutput / totalOutputWorkTime

            self.statusLabelList[1].display(averageSludgeInputPerHour)
            self.statusLabelList[9].display(averageSludgeOutputPerHour)

        except:
            pass

          

        # 평균 투입/배출량

        totalInputWaterRateTime = (len(data) - totalZeroInputWaterRate) 
        totalOutputWaterRateTime = (len(data) - totalZeroOutputWaterRate)

        print('totalWaterRate %d %d'%(totalInputWaterRateTime, totalOutputWaterRateTime))
        
        try:

            averageInputWaterRate = totalInputWaterRate / totalInputWaterRateTime 
            averageOutputWaterRate = totalOutputWaterRate / totalOutputWaterRateTime 

            self.statusLabelList[5].display(averageInputWaterRate)
            self.statusLabelList[7].display(averageOutputWaterRate)

        except:
            pass

        print('total %d %d'%(totalInputWaterRate, totalOutputWaterRate))

        



        # 평균 일 투입량 / 배출량

        current = datetime.datetime.now()
        current = datetime.datetime(current.year, current.month, current.day, 0, 0, 0)
        ago = current - datetime.timedelta(days=int(self.parent.inputDay.text()))

        totalInput = 0.0
        totalOutput = 0.0

        try:
            data = getData.getDataInRange('InfoData','timeData', str(ago), str(current),self.parent.machineName)

        except:
            return 'error'


        for i in data:
            totalInput = totalInput + i['sludgeInput'] 
            totalOutput = totalOutput + i['sludgeOutput']
           

        totalInput = totalInput / int(self.parent.inputDay.text()) / 1000
        totalOutput = totalOutput / int(self.parent.inputDay.text()) / 1000

        self.statusLabelList[2].display(totalInput)
        self.statusLabelList[10].display(totalOutput)
               

              




        