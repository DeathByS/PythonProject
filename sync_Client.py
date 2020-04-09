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
        self.connectIp = "kwtkorea.iptime.org"
        

    def connectClient(self, connectIp="kwtkorea.iptime.org", port=502):
        self.connectIp = connectIp
        print(self.connectIp)
        if self.client is None:
            
            try:
                self.client = ModbusClient(self.connectIp, port) 
                print(self.client)
                if self.client.connect():
                    print("after connect", self.client)
                    return self.client    
                else:
                   print("self.client")
                   return "error"
                    
            except:
                print("error")
                return "error"
        
       

        

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
                return False

        except:
            return False
        # print("rr.coil", readCoils.bits)
        
        

    def readRegister(self, startBit=0, count =15):

        # log.debug("Write to a Coil and read back")
        if self.client is not None:

            try:
        # rq = client.write_coil(0, False, unit=UNIT)
              
        # assert(rr.bits[0] == True)          # test the expected value
        # log.debug("Write to a holding register and read back")
        # rq = client.write_register(30, 10, unit=UNIT)
                readHoldingRegs = self.client.read_holding_registers(startBit, count, unit=UNIT)
                # print("rr.registers", readHoldingRegs.registers)

                return readHoldingRegs.registers
            except:
                print("read error")
                return False
        # assert(not rq.isError())     # test that we are not an error
        # print("rr.registers", rr.registers)
        # ----------------------------------------------------------------------- #
        # close the client
        # ----------------------------------------------------------------------- #
        # self.client.close()
        # time.sleep(2)
           
        else:
            print("check connect")
            return 1
        # return 

# 코드가 인터프리터에 의해 직접 실행 될 때 실행되는 부분
if __name__ == "__main__":
    test = SyncClient()
    test.connectClient(connectIp='kwtujb.iptime.org')
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