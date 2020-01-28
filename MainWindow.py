# coding: utf-8
 
import sys
import csv


from PyQt5 import QtWidgets
from PyQt5 import uic
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtCore import QModelIndex
from sync_Client import SyncClient 
from PyQt5.QtCore import QTimer
from MainWindowInfoTab import MainWindowInfoTab
from MainWindowStatusTab import MainWindowStatusTab
from MainWindowAlarmTab import MainWindowAlarmTab
from MainWindowOperatingTimeTab import MainWindowOperatingTimeTab

 
class MainWindow(QtWidgets.QDialog):
    def __init__(self):
        # QtWidgets.QDialog.__init__(self, parent)
        
        #         super().__init__() uic.loadUi('MainForm.ui', self)
        #  closeEvent 사용을 하려면 self.ui에 form을 load 하는것이 아니라 자기 자신에게 Form을 로드해야됨.
        super().__init__()
        uic.loadUi('MainForm.ui', self)

        # self.ui.tabWidget.addTab(MainWindowTab1(), MainWindowTab1.__name__)
        # self.ui.tabWidget.addTab(MainWindowTab1(), MainWindowTab1.__name__)
       
        # 메인윈도우에 실린 위젯을 조작하기 위해서, 메인윈도우를 부모로 보내어 다른 클래스에서 조작할 수 있게 만든다.
        self.mainWindowInfoTab = MainWindowInfoTab(self)
        self.mainWindowStatusTab = MainWindowStatusTab(self)
        self.mainWindowAlarmTab = MainWindowAlarmTab(self)
        self.mainWindowOperatingTimeTab = MainWindowOperatingTimeTab(self)
        
        # self.mainWindowAlarmTab.insertAlarmList()
        # MainWindowTab1.init_widget(self)

        # plc 와 연결하여 plc Data를 받아오는 객체
        self.plcConnect = SyncClient()
        self.ip = None
        
        # 현장의 기계 A,B,C호기의 시작 주소를 나타내고, 각 탭에서 시작 주소를 통해 A,B,C호기의 데이터를 출력

        self.machineStartReg = 0
        self.machineStartCoil = 0

        

    def connect(self, ip = "kwtkorea.iptime.org"):
        self.plcConnect.connectClient(ip ,502)


    # 각 현장의 A,B,C 호기의 저장 데이터 시작 번지를 설정한다
    def setStartCoilandReg(self, coil, reg):
        self.machineStartCoil = coil
        self.machineStartReg = reg


    def closeEvent(self, QCloseEvent):
        print("Enter CloseEvent")
        self.plcConnect.closeClient()
        self.deleteLater()
        QCloseEvent.accept()


# if __name__ == '__main__':
#     app = QtWidgets.QApplication(sys.argv)
#     w = MainWindow()
#     sys.exit(app.exec())
   