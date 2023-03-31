#!/usr/bin/env python
import can
import time
import cantools
from can.message import Message
from threading import Thread
import keyboard

db = cantools.db.load_file('D:/DCU15_IG/DB/GN7_M/ECANFD_GN7_M.0.dbc')

def Thread_1(id, value):

    bus = can.interface.Bus(bustype = 'vector', channel = 0)

    while(1):
        try:
            msg = db.get_message_by_name('CLU_01_20ms')
            msg_data = msg.encode({'CLU_DisSpdVal':value, 'CLU_DisSpdDcmlVal':0, 'CLU_SpdUnitTyp':0, 'CLU_AlvCnt1Val':0, 'CLU_Crc1Val':65535})
            msg = can.Message(arbitration_id = msg.frame_id, data = msg_data, is_fd = True, is_extended_id = False)

            if keyboard.is_pressed("1"):
                bus.send(msg)
                time.sleep(0.01)
        except can.CanError:
            print("Message NOT sent")
            
def Thread_2(id, value):

    msg = db.get_message_by_name('CLU_02_100ms')
    msg_data = msg.encode({'CLU_DrvngModSwSta':value, 'CLU_OdoVal':0.0, 'CLU_AlvCnt2Val':0, 'CLU_Crc2Val':65535})

    bus = can.interface.Bus(bustype = 'vector', channel = 0)
    msg = can.Message(arbitration_id = msg.frame_id, data = msg_data, is_fd = True, is_extended_id = False)

    while(1):
        try:
            if keyboard.is_pressed("1"):
                bus.send(msg)
                time.sleep(0.01)
        except can.CanError:
            print("Message NOT sent")
            
if __name__ == "__main__":
    
    value1 = 10
    value2 = 1
    th1 = Thread(target = Thread_1, args = (1, value1))
    th2 = Thread(target = Thread_2, args = (2, value2))
    
    th1.start()
    th2.start()
    th1.join()
    th2.join()