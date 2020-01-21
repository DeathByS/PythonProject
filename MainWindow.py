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
        # QTimer 정해진 작업을 정해진 시간마다 반복하게 하기 위해.
        # 여기서는 일정시간에 한번씩 plc에서 Data를 읽어오기 위하여 사용한다.

    def connect(self, ip = "kwtkorea.iptime.org"):
        # com_plcSim
        self.plcConnect.connectClient(ip ,502)
        # plc_1
        # self.plcConnect2.connectClient(ip, 1000) 
        # self.plcWriteObject1.connectClient(ip, 502)

    def closeEvent(self, QCloseEvent):
        print("Enter CloseEvent")
        self.plcConnect.closeClient()
        self.deleteLater()
        QCloseEvent.accept()


# if __name__ == '__main__':
#     app = QtWidgets.QApplication(sys.argv)
#     w = MainWindow()
#     sys.exit(app.exec())
   