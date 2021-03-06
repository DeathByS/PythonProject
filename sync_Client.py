from pymodbus.client.sync import ModbusTcpClient as ModbusClient
from pymodbus.exceptions import ConnectionException
from logging import handlers
import pymodbus
import logging
from time import *

# class FilterMsg(logging.Filter):

#     def filter(self, recode):

#         # logging.debug("Hello")
#         msg = recode.getMessage()
#         time = recode.asctime
#         # print("filter " + time)
        
#         if 'IDLE' in msg:
#             print('filter ' + msg)
#             return True
#         elif 'TRANSACTION_COMPLETE' in msg:
#             return True
        
#         return False


# FILE_MAX_BYTE = 1 * 1024 * 1024
# # FORMAT = ('%(asctime)-15s %(threadName)-15s '
# #           '%(levelname)-8s %(module)-15s:%(lineno)-8s %(message)s')
# FORMAT = ('%(asctime)-15s %(threadName)-15s '
#           '%(levelname)-8s %(message)s')

# LogFormatter = logging.Formatter('%(asctime)-15s %(threadName)-15s '
#           '%(levelname)-8s %(message)s')
# LogHandler = handlers.TimedRotatingFileHandler(filename='log/PLC.log', when='midnight',backupCount=7, interval=1, encoding='utf-8')
# LogHandler.setFormatter(LogFormatter)

# LogHandler.suffix = "%Y%m%d"
# LogHandler.addFilter(FilterMsg())
# streamHander = logging.StreamHandler()
# streamHander.addFilter(FilterMsg())

# logging.basicConfig(format=FORMAT)
# log = logging.getLogger()
# log.setLevel(logging.DEBUG)
# log.addHandler(LogHandler)
# log.addHandler(streamHander)






UNIT = 0x1
class SyncClient:
    def __init__(self):
        self.client = None
        self.connectIp = 0
        

    def connectClient(self, connectIp, port=502, timeout = 1):
        self.connectIp = connectIp
        print(self.connectIp)
        if self.client is None:
            
            try:
                self.client = ModbusClient(self.connectIp, port, timeout = timeout) 
                print(self.client)
                if self.client.connect():
                    print("connect", self.client)
                    return self.client    
                else:
                   print("connect error")
                   return False
                    
            except:
                print("connect error")
                return False 

    def closeClient(self):
        if self.client is not None:
            self.client.close()
            self.client = None

    def writeCoils(self, startCoil=0, data=[False]*6):
        
        if(startCoil is None):
            print("start bit is Null")
            return
        else:
            self.client.write_coils(startCoil, data)
            

    def writeRegisters(self, startRegister=600, data=[1]*15):
        try:
            self.client.write_registers(startRegister, data, unit=UNIT)
        except:
            return False

    def readCoil(self, startBit=0, endBit=26):
        
        try:
            readCoils = None
        
            readCoils = self.client.read_coils(startBit, endBit, unit=UNIT) 

            if(readCoils != None):
                return readCoils.bits
            else:
                print("read Coil error")
                return False
        except:
            return False
        # print("rr.coil", readCoils.bits)
        
    def readRegister(self, startBit=0, count =15):
        # log.debug("Write to a Coil and read back")
        if self.client is not None:
            try:
                readHoldingRegs = self.client.read_holding_registers(startBit, count, unit=UNIT)
                return readHoldingRegs.registers
            except:
                print("read Register error")
                return False 
        else:
            print("check connect")
            return False
        # return 

# 코드가 인터프리터에 의해 직접 실행 될 때 실행되는 부분
if __name__ == "__main__":
    test = SyncClient()
    test.connectClient(connectIp='61.146.82.9')
    # while True:
    holdingRegitsters = test.readRegister()
        # coils = test.readCoil()
        # test.writeCoils()
        # test.closeClient()

    print(holdingRegitsters)

    coils = test.readCoil()
        # coils = test.readCoil()
        # test.writeCoils()
        # test.closeClient()

    print(coils)

    holdingRegitsters = test.readRegister()
        # coils = test.readCoil()
        # test.writeCoils()
        # test.closeClient()

    print(holdingRegitsters)

    holdingRegitsters = test.readRegister()
        # coils = test.readCoil()
        # test.writeCoils()
        # test.closeClient()

    print(holdingRegitsters)
        # sleep(3)