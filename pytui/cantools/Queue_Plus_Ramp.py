#!/usr/bin/env python
import can
import cantools
from can.message import Message
from threading import*
import queue
import time
import keyboard

db = cantools.db.load_file('D:/DCU15_IG/DB/GN7_M/ECANFD_GN7_M.0.dbc')

def Send_CAN(q):

    bus = can.interface.Bus(bustype = 'vector', channel = 0)

    msg_1 = db.get_message_by_name('CLU_01_20ms')
    msg_data_1 = msg_1.encode({'CLU_DisSpdVal':0, 'CLU_DisSpdDcmlVal':0, 'CLU_SpdUnitTyp':0, 'CLU_AlvCnt1Val':0, 'CLU_Crc1Val':65535})

    while(1):
        if not q.empty():
             msg_data_1 = q.get(False)
        
        msg = can.Message(arbitration_id = msg_1.frame_id, data = msg_data_1, is_fd = True, is_extended_id = False)

        bus.send(msg)
        
        time.sleep(0.01)
            
def Input_CAN(q):
    print(1)
    msg_1 = db.get_message_by_name('CLU_01_20ms')
    msg_data_1 = msg_1.encode({'CLU_DisSpdVal':0, 'CLU_DisSpdDcmlVal':0, 'CLU_SpdUnitTyp':0, 'CLU_AlvCnt1Val':0, 'CLU_Crc1Val':65535})
    msg_1 = can.Message(arbitration_id = msg_1.frame_id, data = msg_data_1, is_fd = True, is_extended_id = False)
    
    msg_2 = db.get_message_by_name('CLU_02_100ms')
    msg_data_2 = msg_2.encode({'CLU_DrvngModSwSta':1, 'CLU_OdoVal':0.0, 'CLU_AlvCnt2Val':0, 'CLU_Crc2Val':65535})
    msg_2 = can.Message(arbitration_id = msg_2.frame_id, data = msg_data_2, is_fd = True, is_extended_id = False)

    key = 0
    vel = 0
    
    # if keyboard.is_pressed("1"): key = 1
    # if keyboard.is_pressed("2"): key = 2
    # if keyboard.is_pressed("3"): key = 3
    # if keyboard.is_pressed("4"): key = 4
    # if keyboard.is_pressed("5"): key = 5
    # if keyboard.is_pressed("6"): key = 6

    key = 1
    while(key != 6):
        
        if (vel < 201):
            vel = vel + 1
                
        msg_3 = db.get_message_by_name('CLU_01_20ms')
        msg_data_3 = msg_3.encode({'CLU_DisSpdVal':vel, 'CLU_DisSpdDcmlVal':0, 'CLU_SpdUnitTyp':0, 'CLU_AlvCnt1Val':0, 'CLU_Crc1Val':65535})
        msg_3 = can.Message(arbitration_id = msg_3.frame_id, data = msg_data_3, is_fd = True, is_extended_id = False)
        
        # if keyboard.is_pressed("1"): key = 1
        # if keyboard.is_pressed("2"): key = 2
        # if keyboard.is_pressed("3"): key = 3
        # if keyboard.is_pressed("4"): key = 4
        # if keyboard.is_pressed("5"): key = 5
        # if keyboard.is_pressed("6"): key = 6
        
        if(key == 1): 
            vel = 0
            q.put(msg_data_1)
            time.sleep(0.008)
        if(key == 2): 
            vel = 0
            q.put(msg_2)
            time.sleep(0.008)
        if(key == 3): 
            vel = 0
            q.put(msg_1)
            q.put(msg_2)
            time.sleep(0.008)
        if(key == 4): 
            if (vel > 200):
                key = 5
            q.put(msg_3)
            time.sleep(0.008)
        if(key == 5): 
            while(key == 5):
                vel = 0
                if keyboard.is_pressed("1"): key = 1
                if keyboard.is_pressed("2"): key = 2
                if keyboard.is_pressed("3"): key = 3
                if keyboard.is_pressed("4"): key = 4
                if keyboard.is_pressed("5"): key = 5
                if keyboard.is_pressed("6"): key = 6
             
if __name__ == "__main__":
    
    q = queue.Queue()

    th1 = Thread(target = Send_CAN, args = (q,))
    th2 = Thread(target = Input_CAN, args = (q,))

    th1.start()
    # th1.join()
    th2.start()
    # th2.join()