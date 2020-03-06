# coding: utf-8

from PyQt5 import QtWidgets, Qt
from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QTabWidget, QLabel, QFrame, QTextEdit, QLineEdit, QPushButton
from PyQt5 import uic
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtCore import QModelIndex
from PyQt5.QtCore import QTimer
from enums import OperatingTime
from enums import OpTimeTab
from SingletonInstance import EmailSender
import time
import requests

class MainWindowOperatingTimeTab(QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)   
        
        # MainWindow 폼의 위젯을 조작할 것이기 때문에 MainWindow를 parent로 받아 MainWindow의 위젯을 조작함
        self.parent = parent
        self.opLabelList = []
        self.timeLabelList = []
        self.refTimeLineEditList = []
        self.alarmTimeLineEditList = []
        self.alarmCheck = [False] * 7
        
        self.timer = QTimer(self)
        self.timer.setInterval(5000)
        self.timer.start()
        self.timer.timeout.connect(self.changeTimeLabel)
        self.timer.timeout.connect(self.changePartAlarmOccur)

        self.timer2 = QTimer(self)
        self.timer2.setInterval(1000 * 60 * 1)
        self.timer2.start()
        self.timer2.timeout.connect(self.initAlarmCheck)
       
        self.addedRowDict = {}
        self.colIndex = 0

        self.initWidget()

        # self.emailSender = EmailSender.instance()
 
        self.parent.pushButton_insertRow.clicked.connect(self.insertRowButtonClicked)
        self.parent.pushButton_confirm.clicked.connect(self.confirmButtonClick)
   
   
    def initWidget(self):
        # plc에서 직접 송신하는 값 받는 라벨

        for i in range(1, OpTimeTab.NUMBEROFLABELS.value + 1):
            # 오브젝트의 이름을 가지고 오브젝트 찾아 사용하는법.
            opLabelName = "label_op_%d" % i
            self.opLabelList.append(self.parent.findChild(QtWidgets.QLabel, opLabelName))

            LabelName = "label_Time_%d" % i
            self.timeLabelList.append(self.parent.findChild(QtWidgets.QLabel, LabelName))
            
            refLineEditName = "lineEdit_Standard_%d"%i
            self.refTimeLineEditList.append(self.parent.findChild(QtWidgets.QLineEdit, refLineEditName))

            alarmTimeLineEdiName = "lineEdit_Alarm_%d"%i
            self.alarmTimeLineEditList.append(self.parent.findChild(QtWidgets.QLineEdit, alarmTimeLineEdiName))

            # for i in range(0 , len(self.timeLabelList)):
            #     self.alarmCheck[i] = False


        #사용자 추가 row(db에 저장되어있는걸 읽어와서 추가한다.)

        url = 'http://kwtkorea.iptime.org:8080/OperatingData/?machineName=%s'%self.parent.machineName
        response = requests.get(url=url)
        responseData = response.json()

        if len(responseData) == 0:
            return

        else:

            for i in responseData:

                self.insertRow(i['opName'], i['totalOpTime'], i['referenceTime'], i['alarmTime'], int(i['colIndex']))


            self.colIndex = responseData[-1]['colIndex'] +1
            # print('colIdx : %d'%self.colIndex)

    def changeTimeLabel(self):
        timeList = self.parent.plcConnect.readRegister(self.parent.machineStartReg + OperatingTime.TOTALMIN.value, 
                                                        OperatingTime.FILTERHOUR.value - OperatingTime.TOTALMIN.value + 1)

        timeListIndex = 0

        # print(timeList)
        
        for i in range(1, OperatingTime.FILTERHOUR.value - OperatingTime.TOTALMIN.value + 2, 2):
            # print(i)
            timeText = str(timeList[i])
            self.timeLabelList[timeListIndex].setText(timeText)
            timeListIndex = timeListIndex + 1 

            # if(timeList[i] >= 100):
            #     self.parent.mainWindowAlarmTab.insertAlarm('교체 임박')

    def changePartAlarmOccur(self):
        emailSender = EmailSender.instance()

        for i in range(0 , len(self.timeLabelList)):
            try:
                if self.alarmCheck[i] == False:

                    if int(self.timeLabelList[i].text()) >= int(self.refTimeLineEditList[i].text()):
                        if int(self.timeLabelList[i].text()) < int(self.alarmTimeLineEditList[i].text()):
                            text = self.opLabelList[i].text() + ' 교체 준비'
                            
                            self.alarmCheck[i] = True
                            self.parent.insertAlarm(text)

                        if int(self.timeLabelList[i].text()) >= int(self.alarmTimeLineEditList[i].text()):
                            text = self.opLabelList[i].text() + ' 교체 필요'
                            self.alarmCheck[i] = True
                            self.parent.insertAlarm(text)
                            
            except:
                continue

        for i in self.addedRowDict.keys():
            # print('addrowdic alarm ',self.addedRowDict[i][1].text(), self.addedRowDict[i][2].text(), self.addedRowDict[i][3].text(), str(self.addedRowDict[i][7]))
            try:
                if self.addedRowDict[i][7] == False:

                    if int(self.addedRowDict[i][1].text()) >= int(self.addedRowDict[i][2].text()):
                        print('if 1')
                        if int(self.addedRowDict[i][1].text()) < int(self.addedRowDict[i][3].text()):
                            print('if 2')
                            text = self.addedRowDict[i][0].toPlainText() + ' 교체 준비'
                            self.addedRowDict[i][7] = True
                            self.parent.insertAlarm(text)
                            emailSender.emailSend(subject='Test Email', msg='Test')
                        # print('addrowdic alarm ',self.addedRowDict[i][1].text(), self.addedRowDict[i][2].text(), self.addedRowDict[i][3].text(), str(self.addedRowDict[i][7]))
                        if int(self.addedRowDict[i][1].text()) >= int(self.addedRowDict[i][3].text()):
                            text = self.addedRowDict[i][0].toPlainText() + ' 교체 필요'
                            print('if 3')
                            self.addedRowDict[i][7] = True
                            self.parent.insertAlarm(text)
            except:
                print('error shit')
                continue


    @pyqtSlot()  # pyqtSlot 데코레이터는 꼭 필요는 없다. 하지만 메모리 사용 및 호출 속도에서 약간의 이득을 얻을 수 있다.
    
    # row 추가용 버튼
    def insertRowButtonClicked(self):

        self.insertRow(colIndex=self.colIndex)
        self.colIndex+=1

    def initAlarmCheck(self):

        for i in range(0, len(self.alarmCheck)):
            self.alarmCheck[i] = False

        for i in self.addedRowDict.keys():

            self.addedRowDict[i][7] = False   

    def insertRow(self, opName ='', totalOpTime ='1000', refTime ='10000', alarmTime='10000', colIndex = 0):

        row = self.parent.gridLayout_5.rowCount()
        rowItemList = []

        textEdit = QTextEdit() 
        textEdit.setObjectName('textEdit_title_%d'%row)
        textEdit.setText(opName)
        textEdit.setFrameShape(QFrame.WinPanel)
        textEdit.setFrameShadow(QFrame.Sunken)
        textEdit.setAlignment(Qt.Qt.AlignCenter)
        textEdit.setSizePolicy(QtWidgets.QSizePolicy.Ignored, QtWidgets.QSizePolicy.Preferred)
        textEdit.setMinimumSize(0, 72)
        textEdit.setFocusPolicy(Qt.Qt.StrongFocus)
        
        rowItemList.append(textEdit)

        Label = QLabel() 
        Label.setObjectName('label_OpTime_%d'%row)
        Label.setText(str(totalOpTime))
        Label.setFrameShape(QFrame.WinPanel)
        Label.setFrameShadow(QFrame.Sunken)
        Label.setAlignment(Qt.Qt.AlignCenter)
        Label.setSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        Label.setMinimumSize(0, 72)
        rowItemList.append(Label)

        lineEditStandard = QLineEdit()
        lineEditStandard.setObjectName('lineEdit_Standard_%d'%row)
        lineEditStandard.setInputMask('99999')
        lineEditStandard.setText(str(refTime))
        lineEditStandard.setAlignment(Qt.Qt.AlignCenter)
        lineEditStandard.setSizePolicy(QtWidgets.QSizePolicy.Ignored, QtWidgets.QSizePolicy.Preferred)
        rowItemList.append(lineEditStandard)

        lineEditAlarm = QLineEdit()
        lineEditAlarm.setObjectName('lineEdit_alarm_%d'%row)
        lineEditAlarm.setInputMask('99999')
        lineEditAlarm.setText(str(alarmTime))
        lineEditAlarm.setAlignment(Qt.Qt.AlignCenter)
        lineEditAlarm.setSizePolicy(QtWidgets.QSizePolicy.Ignored, QtWidgets.QSizePolicy.Preferred)
        rowItemList.append(lineEditAlarm)

        resetButton = QPushButton()
        resetButton.setObjectName('button_reset_%d'%row)
        resetButton.setText('reset')
        resetButton.setSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred)
        rowItemList.append(resetButton)


        deleteButton = QPushButton()
        deleteButton.setObjectName('button_delete_%d'%row)
        deleteButton.setText('delete')
        deleteButton.setSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred)

        deleteButton.clicked.connect(lambda state, button=deleteButton : self.deleteButtonClick(state, button))

        rowItemList.append(deleteButton)
        
        rowItemList.append(colIndex)

        # 알람 계속 발생하는거 방지용 false = 알람 발생 안함 / true = 알람 발생 / 6시간 정도에 한번씩 초기화
        rowItemList.append(False)

        column = 0
        for i in rowItemList:
            self.parent.gridLayout_5.addWidget(i,row,column)
            column += 1

            if column == 6:
                break

        self.addedRowDict[str(row)] = (rowItemList)


    #row 삭제용 버튼
    @pyqtSlot()
    def deleteButtonClick(self, state, button):
        row = button.objectName().split("_")
        print("obj name : %s"%row)

        if(self.parent.gridLayout_5.columnCount() == 0):
            return


        for column in range(self.parent.gridLayout_5.columnCount()):
            item = self.parent.gridLayout_5.itemAtPosition(int(row[-1]), column)
            
            
            if item is not None:
                item.widget().deleteLater()
                self.parent.gridLayout_5.removeItem(item)
        
        self.parent.gridLayout_5.update()
        print(self.addedRowDict)
        
        url = 'http://kwtkorea.iptime.org:8080/OperatingData/?machineName=%s&opName=%s'%(self.parent.machineName, self.addedRowDict[row[-1]][0].toPlainText())
        response = requests.get(url=url)

        if len(response.json()) != 0:
            
            url = response.json()[0]['url'] 

            response = requests.delete(url=url) 

        del self.addedRowDict[row[-1]]    


    # 수정된 내용을 db에 반영 시키는 '확인' 버튼
    @pyqtSlot()
    def confirmButtonClick(self):
        
        for i in self.addedRowDict:
            print(i, self.addedRowDict[i][0].toPlainText())
            url = 'http://kwtkorea.iptime.org:8080/OperatingData/?machineName=%s&colIndex=%d'%(self.parent.machineName, self.addedRowDict[i][6]) 
            urlInsert = 'http://kwtkorea.iptime.org:8080/OperatingData/'
            response = requests.get(url=url)

            print(response.text)

            print(len(response.json()))

            data = {}

            data['machineName'] = self.parent.machineName
            data['opName']  = self.addedRowDict[i][0].toPlainText()
            data['totalOpTime'] = self.addedRowDict[i][1].text()
            data['referenceTime'] = self.addedRowDict[i][2].text()
            data['alarmTime'] = self.addedRowDict[i][3].text()
            data['colIndex'] = self.addedRowDict[i][6]


            if len(response.json()) == 0:

                response = requests.post(url=urlInsert, data = data)

                print(response)

            else:

                url = response.json()[0]['url'] 

                response = requests.put(url=url, data = data)  

                print(response)
