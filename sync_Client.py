#!/usr/bin/env python
"""
Pymodbus Synchronous Client Examples
--------------------------------------------------------------------------
The following is an example of how to use the synchronous modbus client
implementation from pymodbus.
It should be noted that the client can also be used with
the guard construct that is available in python 2.5 and up::
    with ModbusClient('127.0.0.1') as client:
        result = client.read_coils(1,10)
        print result
"""
# --------------------------------------------------------------------------- #
# import the various server implementations
# --------------------------------------------------------------------------- #
from pymodbus.client.sync import ModbusTcpClient as ModbusClient
# from pymodbus.client.sync import ModbusUdpClient as ModbusClient
# from pymodbus.client.sync import ModbusSerialClient as ModbusClient

# --------------------------------------------------------------------------- #
# configure the client logging
# --------------------------------------------------------------------------- #
import logging
import time

FORMAT = ('%(asctime)-15s %(threadName)-15s '
          '%(levelname)-8s %(module)-15s:%(lineno)-8s %(message)s')
logging.basicConfig(format=FORMAT)
log = logging.getLogger()
log.setLevel(logging.DEBUG)

UNIT = 0x1

def run_sync_client():

    client = ModbusClient('kwtkorea.iptime.org', port=502)
 
    client.connect()

    while 1:
    
        log.debug("Write to a Coil and read back")
        rr = client.read_coils(0, 10, unit=UNIT) 
        assert(rr.bits[0] == True)          # test the expected value
        log.debug("Write to a holding register and read back")
        # rq = client.write_register(1, 10, unit=UNIT)
        rr = client.read_holding_registers(0, 11, unit=UNIT)
        # assert(not rq.isError())     # test that we are not an error
        print("rr.registers[0]", rr.registers)
        time.sleep(2)
    # ----------------------------------------------------------------------- #
    # close the client
    # ----------------------------------------------------------------------- #
    client.close()


if __name__ == "__main__":
    run_sync_client()