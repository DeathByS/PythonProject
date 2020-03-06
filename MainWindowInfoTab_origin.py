# # coding: utf-8

# from PyQt5 import QtWidgets
# from PyQt5.QtWidgets import QWidget
# from PyQt5.QtWidgets import QTabWidget
# from PyQt5 import uic
# from PyQt5.QtCore import pyqtSlot
# from PyQt5.QtCore import QModelIndex
# from PyQt5.QtCore import QTimer
# from enums import Regs, Machine
# import time

# class MainWindowInfoTab(QWidget):
#     def __init__(self, parent=None):
#         QWidget.__init__(self, parent)   
        
#         # MainWindow 폼의 위젯을 조작할 것이기 때문에 MainWindow를 parent로 받아 MainWindow의 위젯을 조작함
#         self.parent = parent
#         self.lcdList = []
#         self.initWidget()

#         self.timer = QTimer(self)
#         self.timer.setInterval(10000)
#         self.timer.start()
#         self.timer.timeout.connect(self.changeLcdNumber)
        
#     def initWidget(self):
#         self.lcdList.append(self.parent.lcdNumber_1)
#         self.lcdList.append(self.parent.lcdNumber_2)
#         self.lcdList.append(self.parent.lcdNumber_3)
#         self.lcdList.append(self.parent.lcdNumber_4)
#         self.lcdList.append(self.parent.lcdNumber_5)
#         self.lcdList.append(self.parent.lcdNumber_6)
#         self.lcdList.append(self.parent.lcdNumber_7)
#         self.lcdList.append(self.parent.lcdNumber_8)
#         self.lcdList.append(self.parent.lcdNumber_9)
#         self.lcdList.append(self.parent.lcdNumber_10)
#         self.lcdList.append(self.parent.lcdNumber_11)
#         self.lcdList.append(self.parent.lcdNumber_12)
#         self.lcdList.append(self.parent.lcdNumber_13)

        
#     def changeLcdNumber(self):
    
#         regs = self.parent.plcConnect.readRegister(self.parent.machineStartReg + Regs.DRUMFRQ.value, 
#                                                    Regs.RIGHTBALANCE.value + 1)
#         #regs 10, 11번 = 슬러지 투입 / 배출량 Kg 단위에서 Ton 단위로 변환
#         regs[Regs.INPUT.value] = regs[Regs.INPUT.value] / 10
#         regs[Regs.OUTPUT.value] = regs[Regs.OUTPUT.value] / 10
#         # 전압 값을 소수점 단위로 나타내기 위해 
#         regs[Regs.DCV.value] = regs[Regs.DCV.value] / 10

#         # 현장 데이터에서 / 10 해줘야 정상 데이터로 표시됨
#         regs[Regs.DRUMFRQ.value] = regs[Regs.DRUMFRQ.value] / 10
#         regs[Regs.PRESSROLLFRQ.value] = regs[Regs.PRESSROLLFRQ.value] / 10
#         regs[Regs.SLUDEGSUPPLYFRQ.value] = regs[Regs.SLUDEGSUPPLYFRQ.value] / 10
#         regs[Regs.SLUDEGSPREADFRQ.value] = regs[Regs.SLUDEGSPREADFRQ.value] / 10
#         regs[Regs.DRUMCOLLINGWATER.value] = regs[Regs.DRUMCOLLINGWATER.value] / 10
#         regs[Regs.TRANSFORMERSTEMP.value] = regs[Regs.TRANSFORMERSTEMP.value] / 10
        
#         # colis2, regs2 = self.parent.plcConnect2.readRegister()
#         print(regs)
#         if regs == 'read error':
#             self.timer.stop()
#             print("read error, check Connect ")
#             return "error"
             
#         else:
#             # self.parent.plcWriteObject1.writePlcData(0, regs)
#             # self.parent.plcWriteObject1.writePlcData(20,regs2)
#             lcdListIndex = 0 
#             # self.lcdList[12].display(11.0)

#             # print("regs length : " + str(len(regs)))
#             # print("lcd length : " + str(len(self.lcdList)))

#             # print("regs 13 : " + str(regs[12]))
#             for i in range(0, len(self.lcdList)):
#                 print("idx : " + str(i) + "value : " + str(regs[lcdListIndex]))
#                 self.lcdList[i].display(float(regs[lcdListIndex]))
                
#                 # 9, 10번 레지스터를 미사용 하므로 건너 뛴다
#                 if i == 7:
#                     lcdListIndex = lcdListIndex + 3
#                 else:
#                     lcdListIndex = lcdListIndex + 1


              




        