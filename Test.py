# # coding: utf-8

import sys
# from sync_Client import SyncClient 
# from PyQt5 import QtWidgets
# from PyQt5.QtCore import QTimer
# from PyQt5 import QtGui
# from PyQt5 import uic   
# from PyQt5 import QtCore
# from PyQt5.QtCore import pyqtSlot
# from PyQt5.QtGui  import QPixmap
# from PyQt5.QtWidgets import QSizePolicy
# from PyQt5.QtWidgets import QFrame
# import time
 
 
# class Form(QtWidgets.QDialog):
#     def __init__(self, parent=None):
#         QtWidgets.QDialog.__init__(self, parent)
#         self.ui = uic.loadUi("form.ui", self)   
#         self.ui.show()
        
#         # plc 와 연결하여 plc Data를 받아오는 객체
#         self.plcConnect = SyncClient()
       
#         # QTimer 정해진 작업을 정해진 시간마다 반복하게 하기 위해.
#         # 여기서는 일정시간에 한번씩 plc에서 Data를 읽어오기 위하여 사용한다.
#         self.timer = QTimer(self)

#         # 버튼
#         self.startButton.clicked.connect(self.slotStartButton)
#         self.stopButton.clicked.connect(self.slotStopButton)
#         self.changeButton.clicked.connect(self.slotChangeButton)

#         # Plc Connect 와 Disconnect 버튼을 반복적으로 누르게 하지 않기 위해 체크하는 변수
#         self.isStart = False

#         # ip 
#         self.ip = "kwtkorea.iptime.org"

#         #image Label 
#         pixmap = QPixmap("offImage.jpg")
#         self.imageLabel.setFrameStyle(QFrame.Panel | QFrame.Sunken)
#         self.imageLabel.setSizePolicy(QSizePolicy.Ignored,QSizePolicy.Ignored)
#         self.imageLabel.setScaledContents(True)
#         self.ui.imageLabel.setPixmap(QPixmap(pixmap))

#         # lcd Panel control
#         self.ui.lcdNumber_3.display(20.5)
        
#     def changeLabelText(self):
#         coils, regs = self.plcConnect.readRegister()
#         self.ui.testLabel.setText(str(regs[0]))
#         self.ui.lcdNumber_3.display(float(regs[0]))
    
           
#     @pyqtSlot()
#     def slotStartButton(self):
#           if self.isStart == False:
#             self.isStart = True
#             self.plcConnect.connectClient(self.ip)
#             self.timer.setInterval(2000)
#             self.timer.start()
#             self.timer.timeout.connect(self.changeLabelText)
        
#     @pyqtSlot()
#     def slotStopButton(self):
        
#         self.isStart = False
#         self.timer.stop()
#         self.plcConnect.closeClient()
#         #  self.ui.testLabel.setText("2st")
 
#     @pyqtSlot()
#     def slotChangeButton(self):
#          self.ip = self.ui.ipInput.text()
#          self.ui.ipLabel.setText(self.ip)
 
# if __name__ == '__main__':
#     app = QtWidgets.QApplication(sys.argv)
#     w = Form()
#     sys.exit(app.exec())



# import datetime


# current = datetime.datetime.now()

# print(current)

# oneHourago = current - datetime.timedelta(hours=1)

# print(oneHourago)

# import requests

# def getData():

#     urlcompare = 'http://kwtkorea.iptime.org:8080/OperatingData/?opName=종동축 베어링'
#     url = 'http://kwtkorea.iptime.org:8080/OperatingData/'

#     response = requests.get(url=url)

#     print(response.json()[0]['url'].split('/')[-2])

#     print(len(response.json()))

#     if len(response.json()) == 0:
       
#         data = {}
#         data['machineName'] = '의정부_B'
#         data['opName'] = '종동축 베어링' 

#         response = requests.post(url=url, data = data)

#         print(response)
#     else:
#         url = response.json()[0]['url']

#         data = {}
#         data['machineName'] = '의정부_C'
#         data['opName'] = '주동축 베어링'
        
#         response = requests.put(url=url, data = data)

#         print(response)

#     return 0

from sync_Client import SyncClient

def test():
    plc = SyncClient()

    for i in range(0, 10):
        connect = plc.connectClient(connectIp='kwtujb.iptime.org')

        print(connect)

    return 0

if __name__ == '__main__':
    w = test()
    sys.exit(w)