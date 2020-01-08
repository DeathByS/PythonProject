# coding: utf-8
 
import sys
import csv

from PyQt5 import QtWidgets
from PyQt5 import uic
from PyQt5.QtCore import pyqtSlot
from MainWindow import MainWindow
from PyQt5.QtCore import QModelIndex
from PyQt5 import QtGui


 
class Form(QtWidgets.QDialog):
    def __init__(self, parent=None):
        QtWidgets.QDialog.__init__(self, parent)
        self.ui = uic.loadUi("ConnectForm.ui")
        self.ui.show()
        self.connectListDict = {}
        self.initConnectionList()

        # self.mainWindow = MainWidow()
    
        # exit_action = QtGui.QAction('Exit', self)
        
        self.ui.connectButton.clicked.connect(self.slotConnectButton)

    # 파일에 저장되어있는 연결 위치와 아이피값을 받아와 딕셔너리로 저장 후
    # 첫 페이지의 연결 리스트 선택 항목으로 띄워줌
    def initConnectionList(self):
    
        with open('ConnectionList.csv', 'r', encoding='utf-8') as f:
            rdr = csv.reader(f)
            
            connList = [] 
            
            for row in rdr:
                 connList.append(row)
                #  print(connList)
                 self.ui.connectListBox.addItem(row[0])

            self.connectListDict = dict(connList)
            # print(self.connectListDict)
    
    
    

    @pyqtSlot()
    def slotConnectButton(self):
        connectLocation = self.ui.connectListBox.currentText()
        self.ui.ipLabel.setText(self.connectListDict[connectLocation])
        self.mainWindow = MainWindow()
        self.mainWindow.connect(self.connectListDict[connectLocation])
        self.mainWindow.show()
    


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    w = Form()
    sys.exit(app.exec())
    