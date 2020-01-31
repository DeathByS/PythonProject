from pymodbus.client.sync import ModbusTcpClient as ModbusClient
from pymodbus.exceptions import ConnectionException
from logging import handlers
import pymodbus
import logging

class FilterMsg(logging.Filter):

    def filter(self, recode):

        # logging.debug("Hello")
        msg = recode.getMessage()
        # print("filter "+msg)

        if 'transaction' in msg:
            return True
        elif 'Transaction' in msg:
            return True
        # else:
            # return False


FILE_MAX_BYTE = 1 * 1024 * 1024
# FORMAT = ('%(asctime)-15s %(threadName)-15s '
#           '%(levelname)-8s %(module)-15s:%(lineno)-8s %(message)s')
FORMAT = ('%(asctime)-15s %(threadName)-15s '
          '%(levelname)-8s %(message)s')

LogFormatter = logging.Formatter('%(asctime)-15s %(threadName)-15s '
          '%(levelname)-8s %(message)s')
LogHandler = handlers.TimedRotatingFileHandler(filename='PLC.log', when='midnight', interval=1, encoding='utf-8')
LogHandler.setFormatter(LogFormatter)

LogHandler.suffix = "%Y%m%d"
LogHandler.addFilter(FilterMsg())

logging.basicConfig(format=FORMAT)
# logging.root.addFilter(FilterMsg())
log = logging.getLogger()
log.setLevel(logging.DEBUG)
log.addHandler(LogHandler)



# msg = log.callHandlers()
# # text = msg.getMessage()

UNIT = 0x1
class SyncClient:
    def __init__(self):
        self.client = None
        self.connectIp = "kwtkorea.iptime.org"
        

    def connectClient(self, connectIp="kwtkorea.iptime.org", port=502):
        self.connectIp = connectIp

        if self.client is None:
            
            try:
             self.client = ModbusClient(self.connectIp, port) 
             if self.client.connect() is None:
                 print("self.client")
                 return "error"
            except pymodbus.exceptions.ConnectionException: 
             print("error")
             return "error"
        
        print("after connect", self.client)

        return self.client

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
        self.client.write_registers(startRegister, data, unit=UNIT)

    def readCoil(self, startBit=0, endBit=26):
        
        readCoils = self.client.read_coils(startBit, endBit, unit=UNIT) 
        # print("rr.coil", readCoils.bits)
        
        return readCoils.bits

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
            except:
                print("read error")
                return "read error", "read error"
        # assert(not rq.isError())     # test that we are not an error
        # print("rr.registers", rr.registers)
        # ----------------------------------------------------------------------- #
        # close the client
        # ----------------------------------------------------------------------- #
        # self.client.close()
        # time.sleep(2)
            return readHoldingRegs.registers
        else:
            print("check connect")
            return 1
        # return 

# 코드가 인터프리터에 의해 직접 실행 될 때 실행되는 부분
if __name__ == "__main__":
    test = SyncClient()
    test.connectClient()
    holdingRegitsters = test.readRegister()
    coils = test.readCoil()
    # test.writeCoils()
    # test.closeClient()

    print(coils, holdingRegitsters)