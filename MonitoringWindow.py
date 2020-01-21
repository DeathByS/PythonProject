# coding: utf-8
 
import sys
import csv

from PyQt5 import QtWidgets
from PyQt5 import uic
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtCore import QModelIndex
from sync_Client import SyncClient 
from PyQt5.QtCore import QTimer
from enums import Coils
from MainWindow import MainWindow
 
class MonitoringWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('MonitoringForm.ui', self)

        self.plcConnectList = [] 
        self.ip = None
        # QTimer 정해진 작업을 정해진 시간마다 반복하게 하기 위해.
        # 여기서는 일정시간에 한번씩 plc에서 Data를 읽어오기 위하여 사용한다.
        self.statusLabelList = []
        self.label_1.setText("AAA")

        self.connectListDict = {}
        self.initConnectionList()
        self.initStatusLabel()

        self.initPlcConnect()

        self.changeStatusLabel()

        self.pushButton_1.clicked.connect(lambda state, button=self.pushButton_1 : self.slotConnectButton(state, button))
        self.pushButton_2.clicked.connect(lambda state, button=self.pushButton_2 : self.slotConnectButton(state, button))

        

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
            self.plcConnectList.append(self.connect(self.connectListDict[i]))


    def initStatusLabel(self):
        self.statusLabelList.append(self.label_1)
        self.statusLabelList.append(self.label_5)

    def connect(self, ip = "kwtkorea.iptime.org"):
        plcConnect = SyncClient()
        plcConnect.connectClient(ip, 502)
        return plcConnect

    def changeStatusLabel(self):
        print("changes")
        index = 0
        
        for i in range(0, 2):
            # print(i)
            onoff = self.plcConnectList[i].readCoil(Coils.AUTOMATICSTART.value, Coils.AUTOMATICSTART.value + 10)

            print(onoff[0])
            if onoff[0] is True:
                onoff = 'On'
            else:
                onoff = 'Off'

            self.statusLabelList[i].setText(onoff)
            
            
    @pyqtSlot()
    def slotConnectButton(self, state, button):
        connLocation = button.text()
        self.mainWindow = MainWindow()
        self.mainWindow.connect(self.connectListDict[connLocation])
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
   