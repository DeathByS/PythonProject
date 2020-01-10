from pymodbus.client.sync import ModbusTcpClient as ModbusClient
from pymodbus.exceptions import ConnectionException
from logging import handlers
import pymodbus
import logging

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

logging.basicConfig(format=FORMAT)
log = logging.getLogger()
log.setLevel(logging.DEBUG)
log.addHandler(LogHandler)

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
    def writePlcData(self, startRegister=600, data=[1]*15):
        self.client.write_registers(startRegister, data, unit=UNIT)


    def readPlcData(self):

        log.debug("Write to a Coil and read back")
        if self.client is not None:

            try:
        # rq = client.write_coil(0, False, unit=UNIT)
                readCoils = self.client.read_coils(0, 10, unit=UNIT) 
                print("rr.coil", readCoils.bits)
        # assert(rr.bits[0] == True)          # test the expected value
        # log.debug("Write to a holding register and read back")
        # rq = client.write_register(30, 10, unit=UNIT)
                readHoldingRegs = self.client.read_holding_registers(0, 15, unit=UNIT)
                print("rr.registers", readHoldingRegs.registers)
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
            return readCoils.bits, readHoldingRegs.registers
        else:
            print("check connect")
            return 1
        # return 

# 코드가 인터프리터에 의해 직접 실행 될 때 실행되는 부분
# if __name__ == "__main__":
   


# test = SyncClient()

# test.connectClient()

# coils, holdingRegitsters = test.runSyncClient()

# test.closeClient()

# print(coils, holdingRegitsters)