# coding: utf-8
 
import sys
import csv

from PyQt5 import QtWidgets
from PyQt5 import uic
from PyQt5.QtCore import pyqtSlot
from MainWindow import MainWindow
from PyQt5.QtCore import QModelIndex


 
class Form(QtWidgets.QDialog):
    def __init__(self, parent=None):
        QtWidgets.QDialog.__init__(self, parent)
        self.ui = uic.loadUi("ConnectForm.ui")
        self.ui.show()
        self.connectListDict = {}
        self.initConnectionList()

        # self.mainWindow = MainWidow()
    
        
        self.ui.connectButton.clicked.connect(self.slotConnectButton)

    # 파일에 저장되어있는 연결 위치와 아이피값을 받아와 딕셔너리로 저장 후
    # 첫 페이지의 연결 리스트 선택 항목으로 띄워줌
    def initConnectionList(self):
    

        # 오류가 난 이유(시도 해볼 것 ) list로 정확하게 만든 후 a_list.append(row) 이런 식으로 시도해 볼 것 
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
        # self.ui.stackedWidget.setCurrentIndex(1)
        self.mainWindow = MainWindow()
        self.mainWindow.ui.show()



if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    w = Form()
    sys.exit(app.exec())