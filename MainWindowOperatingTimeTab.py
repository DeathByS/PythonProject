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
from datetime import datetime
import time
import requests
import csv

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
        self.timer2.setInterval(1000 * 60 * 5)
        self.timer2.start()
        self.timer2.timeout.connect(self.initAlarmCheck)
       
        self.addedRowDict = {}
        self.colIndex = 0

        self.initWidget()

        # self.emailSender = EmailSender.instance()
 
        self.parent.pushButton_insertRow.clicked.connect(self.insertRowButtonClicked)
        
        self.parent.pushButton_confirm.setAutoRepeat(True)
        self.parent.pushButton_confirm.setAutoRepeatInterval(10)
        self.parent.pushButton_confirm.pressed.connect(self.confirmButtonClick)
       
        # self.parent.pushButton_confirm.pressed.connect(self.confirmButtonClick)
   
   
    def initWidget(self):
        # plc에서 직접 송신하는 값 받는 라벨
        OpAlarmTimeList = [] 
        
        try:
            with open('data/OpAlarmTime_%s.csv'%self.parent.machineName, 'r', encoding='utf-8') as f:
                rdr = csv.reader(f)
                for row in rdr:
                    OpAlarmTimeList.append(row)
        except:
            print('file not found')
            pass

        for i in range(1, OpTimeTab.NUMBEROFLABELS.value + 1):
            # 오브젝트의 이름을 가지고 오브젝트 찾아 사용하는법.
            opLabelName = "label_op_%d" % i
            self.opLabelList.append(self.parent.findChild(QtWidgets.QLabel, opLabelName))

            LabelName = "label_Time_%d" % i
            self.timeLabelList.append(self.parent.findChild(QtWidgets.QLabel, LabelName))
            
            refLineEditName = "lineEdit_Standard_%d"%i
            refLineEdit = self.parent.findChild(QtWidgets.QLineEdit, refLineEditName)
            if len(OpAlarmTimeList):
                refLineEdit.setText(OpAlarmTimeList[i-1][0])
            else:
                refLineEdit.setText(str(10000))
            self.refTimeLineEditList.append(refLineEdit)

            alarmTimeLineEditName = "lineEdit_Alarm_%d"%i
            alarmTimeLineEdit = self.parent.findChild(QtWidgets.QLineEdit, alarmTimeLineEditName)
            if len(OpAlarmTimeList):
                alarmTimeLineEdit.setText(OpAlarmTimeList[i-1][1])
            else:
                alarmTimeLineEdit.setText(str(20000))
            self.alarmTimeLineEditList.append(alarmTimeLineEdit)

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
                startTime = datetime.strptime(i['startingTime'], '%Y-%m-%d %H:%M:%S.%f')
                currentTime = datetime.now()

                ago = currentTime - startTime 
                agoHour = int((ago.days * 24) + (ago.seconds / 3600))
                self.insertRow(i['opName'], agoHour, i['referenceTime'], i['alarmTime'], int(i['colIndex']), startTime)


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
        for i in self.addedRowDict.keys():
            startTime = datetime.strptime(str(self.addedRowDict[i][7]), '%Y-%m-%d %H:%M:%S.%f')
            currentTime = datetime.now()

            ago = currentTime - startTime 
            agoHour = int((ago.days * 24) + (ago.seconds / 3600))

            self.addedRowDict[i][1].setText(str(agoHour))

    def changePartAlarmOccur(self):
        emailSender = EmailSender.instance()
        emailReciver = self.parent.lineEdit_replacePartEmail.text()
        location = self.parent.machineName

        for i in range(0 , len(self.timeLabelList)):
            try:
                if self.alarmCheck[i] == False:

                    if int(self.timeLabelList[i].text()) >= int(self.refTimeLineEditList[i].text()):
                        if int(self.timeLabelList[i].text()) < int(self.alarmTimeLineEditList[i].text()):
                            text = self.opLabelList[i].text() + ' 교체 준비'
                            self.alarmCheck[i] = True
                            self.parent.insertAlarm(text)
                            subject = '한국워터테크놀로지 부품 교체 준비 알림 메일입니다.'
                            msg = '기기 이름 : %s\n 교체 준비 부품 : %s \n 부품 재고를 확인해주세요' %(location,
                            self.opLabelList[i].text())
                            emailSender.emailSend(reciver=emailReciver,subject=subject, msg=msg)
                            time = datetime.now()
                            with open("log/ChangePartAlarmLog.txt", "at", encoding='utf-8') as f:
                                f.write(str(time) + ' %s %s 부품 교체 준비 알람 메일 발송\n'%(location, self.opLabelList[i].text()))
                            self.parent.setNumberOfPartChangeAlarm(1)

                        if int(self.timeLabelList[i].text()) >= int(self.alarmTimeLineEditList[i].text()):
                            text = self.opLabelList[i].text() + ' 교체 필요'
                            self.alarmCheck[i] = True
                            self.parent.insertAlarm(text)

                            subject = '한국워터테크놀로지 부품 교체 필요 알림 메일입니다.'
                            msg = '기기 이름 : %s\n 교체 필요 부품 : %s \n 부품을 교체해주세요' %(location,
                            self.opLabelList[i].text())
                            emailSender.emailSend(reciver=emailReciver,subject=subject, msg=msg)
                            time = datetime.now()
                            with open("log/ChangePartAlarmLog.txt", "at", encoding='utf-8') as f:
                                f.write(str(time) + ' %s %s 부품 교체 필요 알람 메일 발송\n'%(location, self.opLabelList[i].text()))
                            self.parent.setNumberOfPartChangeAlarm(1)
                            
            except:
                continue

        for i in self.addedRowDict.keys():
            # print('addrowdic alarm ',self.addedRowDict[i][1].text(), self.addedRowDict[i][2].text(), self.addedRowDict[i][3].text(), str(self.addedRowDict[i][7]))
            try:
                # addedRowDict[i][7] = 해당되는 행의 알람이 울렸는지 체크하는 변수
                if self.addedRowDict[i][8] == False:

                    if int(self.addedRowDict[i][1].text()) >= int(self.addedRowDict[i][2].text()):
                       
                        if int(self.addedRowDict[i][1].text()) < int(self.addedRowDict[i][3].text()):
                            text = self.addedRowDict[i][0].toPlainText() + ' 교체 준비'
                            self.addedRowDict[i][8] = True
                            self.parent.insertAlarm(text)
                            subject = '한국워터테크놀로지 부품 교체 준비 알림 메일입니다.'
                            msg = '기기 이름 : %s\n 교체 준비 부품 : %s \n 부품 재고를 확인해주세요' %(location, 
                            self.addedRowDict[i][0].toPlainText())
                            emailSender.emailSend(reciver=emailReciver,subject=subject, msg=msg)

                            time = datetime.now()
                            with open("log/ChangePartAlarmLog.txt", "at", encoding='utf-8') as f:
                                f.write(str(time) + ' %s %s 부품 교체 준비 알람 메일 발송\n'%(location, self.addedRowDict[i][0].toPlainText()))
                            self.parent.setNumberOfPartChangeAlarm(1)
                        # print('addrowdic alarm ',self.addedRowDict[i][1].text(), self.addedRowDict[i][2].text(), self.addedRowDict[i][3].text(), str(self.addedRowDict[i][7]))
                        if int(self.addedRowDict[i][1].text()) >= int(self.addedRowDict[i][3].text()):
                            text = self.addedRowDict[i][0].toPlainText() + ' 교체 필요'
                            self.addedRowDict[i][8] = True
                            self.parent.insertAlarm(text)
                            self.parent.setNumberOfPartChangeAlarm(1)
                            subject = '한국워터테크놀로지 부품 교체 필요 알림 메일입니다.'
                            msg = '기기 이름 : %s\n 교체 필요 부품 : %s \n 부품 교체가 필요합니다.' %(location,
                            self.addedRowDict[i][0].toPlainText())
                            emailSender.emailSend(reciver=emailReciver,subject=subject, msg=msg)
                            time = datetime.now()
                            with open("log/ChangePartAlarmLog.txt", "at", encoding='utf-8') as f:
                                f.write(str(time) + ' %s %s 부품 교체 필요 알람 메일 발송\n'%(location, self.addedRowDict[i][0].toPlainText()))
            except:
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

            self.addedRowDict[i][8] = False   

    def insertRow(self, opName ='', totalOpTime ='0', refTime ='8000', alarmTime='10000', colIndex = 0, timeText =''):

        row = self.parent.gridLayout_5.rowCount()
        rowItemList = []

        if(timeText == ''):
            timeText = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
            print('timeText %s'%timeText)

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
        resetButton.clicked.connect(lambda state, button=resetButton : self.resetButtonClicked(state, button))
        resetButton.setStyleSheet('QPushButton::pressed#%s{font: 14pt "맑은 고딕";border-image: url(:/image/label1.png);}'%('button_reset_%d'%row))

        rowItemList.append(resetButton)


        deleteButton = QPushButton()
        deleteButton.setObjectName('button_delete_%d'%row)
        deleteButton.setText('delete')
        deleteButton.setSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred)

        deleteButton.clicked.connect(lambda state, button=deleteButton : self.deleteButtonClicked(state, button))
        deleteButton.setStyleSheet('QPushButton::pressed#%s{font: 14pt "맑은 고딕";border-image: url(:/image/label1.png);}'%('button_delete_%d'%row))

        rowItemList.append(deleteButton)
        
        #6
        rowItemList.append(colIndex)

        #7 
        rowItemList.append(timeText)

        #8번 알람 계속 발생하는거 방지용 false = 알람 발생 안함 / true = 알람 발생 / 6시간 정도에 한번씩 초기화
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
    def deleteButtonClicked(self, state, button):
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
        # print(self.addedRowDict)
        
        url = 'http://kwtkorea.iptime.org:8080/OperatingData/?machineName=%s&opName=%s'%(self.parent.machineName, self.addedRowDict[row[-1]][0].toPlainText())
        response = requests.get(url=url)

        if len(response.json()) != 0:
            
            url = response.json()[0]['url'] 

            response = requests.delete(url=url) 

        del self.addedRowDict[row[-1]]    


    # 수정된 내용을 저장하는 저장 버튼
    @pyqtSlot()
    def confirmButtonClick(self):
        print('in confirmButton')

        # plc에서 직접 값 받아오는 행의 설정 시간 저장

        with open(('data/OpAlarmTime_%s.csv'%self.parent.machineName), 'w', encoding='utf-8', newline='') as f:
            rdr = csv.writer(f)
            
            for (i, j) in zip(self.refTimeLineEditList, self.alarmTimeLineEditList):
                rdr.writerow([int(i.text()), int(j.text())])
                 



        # 추가된 라벨은 db에 저장
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
            # data['startingTime'] = self.addedRowDict[i][7]


            if len(response.json()) == 0:

                response = requests.post(url=urlInsert, data = data)

                print(response)

            else:

                url = response.json()[0]['url'] 

                response = requests.put(url=url, data = data)  

                print(response)
    
    @pyqtSlot()
    # 만들어진 행의 시간을 초기화 시킴
    def resetButtonClicked(self, state, button):
        row = button.objectName().split('_')[-1] 

        print('row %s', row)

        timeText = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
        self.addedRowDict[row][7] = timeText

        url = 'http://kwtkorea.iptime.org:8080/OperatingData/?machineName=%s&colIndex=%d'%(self.parent.machineName, self.addedRowDict[row][6])

        response = requests.get(url=url)

        print(response.text)

        print(len(response.json()))

        data = {}

        # data['machineName'] = self.parent.machineName
        # data['opName']  = self.addedRowDict[i][0].toPlainText()
        # data['totalOpTime'] = self.addedRowDict[i][1].text()
        # data['referenceTime'] = self.addedRowDict[i][2].text()
        # data['alarmTime'] = self.addedRowDict[i][3].text()
        # data['colIndex'] = self.addedRowDict[i][6]
        data['startingTime'] = timeText


        if len(response.json()) == 0:

           pass

        else:

            url = response.json()[0]['url'] 

            response = requests.put(url=url, data = data)  



