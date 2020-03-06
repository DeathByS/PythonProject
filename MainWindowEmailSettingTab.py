from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QTabWidget
from PyQt5 import uic
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtCore import QModelIndex
from PyQt5.QtCore import QTimer
from PyQt5.QtCore import QRegExp
from PyQt5.QtGui  import QRegExpValidator
from enums import Regs, Machine
import time
import requests

class MainWindowEmailSettingTab(QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)   
        
        # MainWindow 폼의 위젯을 조작할 것이기 때문에 MainWindow를 parent로 받아 MainWindow의 위젯을 조작함
        self.parent = parent
        self.emailList = []
        self.initWidget()
        self.timer = QTimer(self)
        self.timer.setInterval(10000)
        self.timer.start()
        # self.timer.timeout.connect(self.changelcdData)

    
        
    def initWidget(self):
        self.replacePartEmail = self.parent.lineEdit_replacePartEmail
        regex = QRegExp("\\b[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,4}\\b")
        validator = QRegExpValidator(regex)
        self.replacePartEmail.setValidator(validator)
        self.sludgeOutEmail = self.parent.lineEdit_sludgeOutEmail
        self.sludgeOutEmail.setValidator(validator)

        self.emailList.append(self.replacePartEmail)
        self.emailList.append(self.sludgeOutEmail)

        self.parent.pushButton_save.clicked.connect(lambda state, button=self.parent.pushButton_save : self.saveButtonClick(state, button))

        try:
            url = 'http://kwtkorea.iptime.org:8080/EmailData/'
            response = requests.get(url=url)

            if len(response.json()) == 0:
                 return
            else:
                self.emailList[0].setText(response.json()[0]['replacePartEmail'])
                self.emailList[1].setText(response.json()[0]['sludgeOutEmail'])
        except:
            pass

        
    @pyqtSlot()
    def saveButtonClick(self, state, button):
        data = {}


        data['machineName'] = self.parent.machineName
        data['replacePartEmail'] = self.emailList[0].text()
        data['sludgeOutEmail'] = self.emailList[1].text()


        # url = 'http://kwtkorea.iptime.org:8080/EmailData/?machineName=%s&%s=%s'%(self.parent.machineName, emailColumn, email) 
        url = 'http://kwtkorea.iptime.org:8080/EmailData/'
        response = requests.get(url=url)
       
        print(response.text)

        print(len(response.json()))

        if len(response.json()) == 0:

            response = requests.post(url=url, data = data)

            print(response)

        else:

            url = response.json()[0]['url'] 

            response = requests.put(url=url, data = data)  

            print(response)
