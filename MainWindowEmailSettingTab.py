from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QTabWidget
from PyQt5 import uic
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtCore import QModelIndex
from PyQt5.QtCore import QTimer
from PyQt5.QtCore import QRegExp
from PyQt5.QtGui  import QRegExpValidator
from enums import Regs, Machine, WriteValue
import time
from datetime import datetime
import requests

class MainWindowEmailSettingTab(QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)   
        print('init MainWindowEmailSettingTab')
        # MainWindow 폼의 위젯을 조작할 것이기 때문에 MainWindow를 parent로 받아 MainWindow의 위젯을 조작함
        self.parent = parent
        self.emailList = []
        self.initWidget()
        # self.timer = QTimer(self)
        # self.timer.setInterval(3000)
        # self.timer.start()
        # self.timer.timeout.connect(self.setSludgeOut)
    
        
    def initWidget(self):
        self.replacePartEmail = self.parent.lineEdit_replacePartEmail
        self.expendablesPartEmail = self.parent.lineEdit_ExpendablesPartEmail
        self.productionPartEmail = self.parent.lineEdit_ProductionPartEmail
        regex = QRegExp("\\b[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,4}\\b")
        validator = QRegExpValidator(regex)
        self.replacePartEmail.setValidator(validator)
        self.expendablesPartEmail.setValidator(validator)
        self.productionPartEmail.setValidator(validator)

        self.sludgeOutEmail = self.parent.lineEdit_sludgeOutEmail
        self.sludgeOutEmail.setValidator(validator)

        self.emailList.append(self.replacePartEmail)
        self.emailList.append(self.expendablesPartEmail)
        self.emailList.append(self.productionPartEmail)
        self.emailList.append(self.sludgeOutEmail)
 
        regexNum = QRegExp("\\b[0-9]+[0-9]")
        validatorNum = QRegExpValidator(regexNum)
        self.parent.lineEdit_sludgeOut.setValidator(validatorNum)


        self.parent.pushButton_save.clicked.connect(lambda state, button=self.parent.pushButton_save : self.saveButtonClick(state, button))
        self.parent.pushButton_out.clicked.connect(lambda state, button=self.parent.pushButton_out : self.outButtonClick(state, button))
        
       
        try:
            url = 'http://kwtkorea.iptime.org:8080/EmailData/?machineName=%s'%self.parent.machineName
            response = requests.get(url=url)

            if len(response.json()) == 0:
                 return
            else:
                self.emailList[0].setText(response.json()[0]['replacePartEmail'])
                self.emailList[1].setText(response.json()[0]['expendablesPartEmail'])
                self.emailList[2].setText(response.json()[0]['productionPartEmail'])
                self.emailList[3].setText(response.json()[0]['sludgeOutEmail'])
                

        except:
            pass


        try:
             # reg 4003 = 배출 슬러지 무게 설정
            value = self.parent.plcConnect.readRegister(WriteValue.SLUDGEOUTWEIGHT.value, 1)
            print(value[0])
            self.parent.lineEdit_sludgeOut.setText(str(value[0]))

       
        except:
            print('error sludgeoutReg')
            pass


    # def setSludgeOut(self):
       
    

        
    @pyqtSlot()
    def saveButtonClick(self, state, button):

        data = {}

        data['machineName'] = self.parent.machineName
        data['replacePartEmail'] = self.emailList[0].text()
        data['expendablesPartEmail'] = self.emailList[1].text()
        data['productionPartEmail'] =  self.emailList[2].text()
        data['sludgeOutEmail'] = self.emailList[3].text()

        # url = 'http://kwtkorea.iptime.org:8080/EmailData/?machineName=%s&%s=%s'%(self.parent.machineName, emailColumn, email) 
        url = 'http://kwtkorea.iptime.org:8080/EmailData/?machineName=%s'%self.parent.machineName
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

        try:
            outValue = int(self.parent.lineEdit_sludgeOut.text())
            print('outValue = %d'%outValue)
            
            self.parent.plcConnect.writeRegisters(WriteValue.SLUDGEOUTWEIGHT.value, [outValue] * 1)
            value = self.parent.plcConnect.readRegister(WriteValue.SLUDGEOUTWEIGHT.value, 1)
            # print(value)
        except:
            return('error setSludgeOut MainWindowEmailSetting')    


    @pyqtSlot()
    def outButtonClick(self, state, button):
        try:
            # coil 8001 = 배출량 초기화용 스위치 변수
            self.parent.plcConnect.writeCoils(WriteValue.SLUDGEOUTRESET.value, [1] *1)
            self.parent.plcConnect.writeCoils(WriteValue.SLUDGEOUTRESET.value, [0] *1)
            location = self.parent.machineName
            starttime = datetime.now()
            with open("log/SludgeOutComplete.txt", "at", encoding='utf-8') as f:    
                f.write(str(starttime) + ' %s 슬러지 배출 완료\n'%(location))
            
        except:
            print('error outButtonClick MainWindowEmailSetting outButtonClicck')
            pass

       