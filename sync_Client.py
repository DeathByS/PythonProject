from pymodbus.client.sync import ModbusTcpClient as ModbusClient
from pymodbus.exceptions import ConnectionException
import pymodbus
import logging


FORMAT = ('%(asctime)-15s %(threadName)-15s '
          '%(levelname)-8s %(module)-15s:%(lineno)-8s %(message)s')
logging.basicConfig(format=FORMAT)
log = logging.getLogger()
log.setLevel(logging.DEBUG)

UNIT = 0x1
class SyncClient:
    def __init__(self):
        self.client = None
        self.connectIp = "kwtkorea.iptime.org"

    def connectClient(self, connectIp="kwtkorea.iptime.org"):
        self.connectIp = connectIp

        if self.client is None:
            
            try:
             self.client = ModbusClient(self.connectIp, port=502) 
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

    def runSyncClient(self):

        log.debug("Write to a Coil and read back")
        if self.client is not None:

            try:
        # rq = client.write_coil(0, False, unit=UNIT)
                readCoils = self.client.read_coils(0, 10, unit=UNIT) 
                print("rr.coil", readCoils.bits)
        # assert(rr.bits[0] == True)          # test the expected value
        # log.debug("Write to a holding register and read back")
        # rq = client.write_register(30, 10, unit=UNIT)
                readHoldingRegs = self.client.read_holding_registers(0, 11, unit=UNIT)
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