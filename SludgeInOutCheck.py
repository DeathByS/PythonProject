from enums import Regs, Machine
from datetime import datetime
import time
import requests



class SludgeInOutCheck():
    def __init__(self, parent=None):
        self.parent = parent

        self.dataCount = 0
        self.receiveTime = []

        self.url = 'http://kwtkorea.iptime.org:8080/SludgeInOutData/'

    def insertSludgeInOut(self):
        
        try:
            beforeTime = datetime.now()
            regs = self.parent.plcConnect.readRegister(self.parent.machineStartReg + Regs.DRUMFRQ.value, 
                                                        Regs.SLIPRINGTEMP.value + 1)
            afterTime = datetime.now()

            location = self.parent.machineName
            receiveTime = (afterTime - beforeTime).microseconds / 1000

            data = {}
            data['machineName'] = location
            data['receiveTime'] = receiveTime
            data['sludgeInput'] = regs[Regs.INPUT.value]
            data['sludgeOutput'] = regs[Regs.OUTPUT.value]

            response = requests.post(url=self.url, data = data)
            print(response.status_code)

            self.receiveTime.append(receiveTime) 
            overTime = [i for i in self.receiveTime if i > 500]
            overTimeCount = len(overTime)  

            with open("log/SludgeInOutLog.txt", "at", encoding='utf-8') as f:
                f.write(str(beforeTime) + ' connect %s\n'%location)
                f.write(str(receiveTime)+'ms\n')
                f.write('%d개의 데이터 전송, 평균 속도 : %.3f 최대 : %.3f\n'%(len(self.receiveTime), 
                sum(self.receiveTime)/len(self.receiveTime), max(self.receiveTime)))
                # 5초당 한번씩 함수를 호출하고, receiveTime = 500ms (0.5초) 이상 되면 초과
                f.write('전송시간 초과 : %d개\n'%overTimeCount)  

        except:
            print('error insertSludgeInout')