# coding: utf-8
 
import sys
import csv
import copy
from PyQt5 import QtWidgets
from PyQt5 import uic
from PyQt5.QtCore import pyqtSlot


 
class Form(QtWidgets.QDialog):
    def __init__(self, parent=None):
        QtWidgets.QDialog.__init__(self, parent)
        self.ui = uic.loadUi("ConnectForm.ui")
        self.ui.show()
        self.connectListDict = {}
        self.initConnectionList()
        
        self.ui.connectButton.clicked.connect(self.slotConnectButton)

    # 파일에 저장되어있는 연결 위치와 아이피값을 받아와 딕셔너리로 저장 후
    # 첫 페이지의 연결 리스트 선택 항목으로 띄워줌
    def initConnectionList(self):
    
        with open('filename.csv', 'r', encoding='utf-8') as f:
            rdr = csv.reader(f)
            self.connectListDict = dict(rdr)
            print(self.connectListDict)
            

        with open('filename.csv', 'r', encoding='utf-8') as f:
            rdr = csv.reader(f)
            for loop in rdr:
                self.ui.connectListBox.addItem(loop[0])

    @pyqtSlot()
    def slotConnectButton(self):
        connectIpLocation = self.ui.connectListBox.currentText()
        self.ui.ipLabel.setText(self.connectListDict[connectIpLocation])



if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    w = Form()
    sys.exit(app.exec())