#!/usr/bin/env python
import can
import cantools
from can.message import Message
from threading import*
import queue
import time
import keyboard

class PythontoTest():
    
    def __init__(self):
        db = cantools.db.load_file('D:/DCU15_IG/DB/GN7_M/ECANFD_GN7_M.0.dbc')
        
        self.msg_1 = db.get_message_by_name('CLU_01_20ms')
        msg_data_1 = self.msg_1.encode({'CLU_DisSpdVal':0, 'CLU_DisSpdDcmlVal':0, 'CLU_SpdUnitTyp':0, 'CLU_AlvCnt1Val':0, 'CLU_Crc1Val':65535})
        self.msg_1 = can.Message(arbitration_id = self.msg_1.frame_id, data = msg_data_1, is_fd = True, is_extended_id = False)
        
        self.msg_2 = db.get_message_by_name('CLU_02_100ms')
        msg_data_2 = self.msg_2.encode({'CLU_DrvngModSwSta':1, 'CLU_OdoVal':0.0, 'CLU_AlvCnt2Val':0, 'CLU_Crc2Val':65535})
        self.msg_2 = can.Message(arbitration_id = self.msg_2.frame_id, data = msg_data_2, is_fd = True, is_extended_id = False)
        
        self.vel = 0
        self.msg_3 = db.get_message_by_name('CLU_01_20ms')
        msg_data_3 = self.msg_3.encode({'CLU_DisSpdVal':self.vel, 'CLU_DisSpdDcmlVal':0, 'CLU_SpdUnitTyp':0, 'CLU_AlvCnt1Val':0, 'CLU_Crc1Val':65535})
        self.msg_3 = can.Message(arbitration_id = self.msg_3.frame_id, data = msg_data_3, is_fd = True, is_extended_id = False)
        

    def Send_CAN(q, self):

        bus = can.interface.Bus(bustype = 'vector', channel = 0)

        while(1):
            bus.send(q.get())
            
            # time.sleep(0.01)
            
    def Input_CAN(q, self):

        key = 0
        
        if keyboard.is_pressed("1"): key = 1
        if keyboard.is_pressed("2"): key = 2
        if keyboard.is_pressed("3"): key = 3
        if keyboard.is_pressed("4"): key = 4
        if keyboard.is_pressed("5"): key = 5
        if keyboard.is_pressed("6"): key = 6

        while(key != 6):
            
            if (self.vel < 201):
                self.vel = self.vel + 1
            
            if keyboard.is_pressed("1"): key = 1
            if keyboard.is_pressed("2"): key = 2
            if keyboard.is_pressed("3"): key = 3
            if keyboard.is_pressed("4"): key = 4
            if keyboard.is_pressed("5"): key = 5
            if keyboard.is_pressed("6"): key = 6
            
            if(key == 1): 
                self.vel = 0
                q.put(self.msg_1)
            if(key == 2): 
                self.vel = 0
                q.put(self.msg_2)
            if(key == 3): 
                self.vel = 0
                q.put(self.msg_1)
                q.put(self.msg_2)
            if(key == 4): 
                if (self.vel > 200):
                    key = 5
                q.put(self.msg_3)
            if(key == 5): 
                while(key == 5):
                    self.vel = 0
                    if keyboard.is_pressed("1"): key = 1
                    if keyboard.is_pressed("2"): key = 2
                    if keyboard.is_pressed("3"): key = 3
                    if keyboard.is_pressed("4"): key = 4
                    if keyboard.is_pressed("5"): key = 5
                    if keyboard.is_pressed("6"): key = 6
            
            time.sleep(0.01) #버튼에 맞게

    q = queue.Queue()

    th1 = Thread(target = Send_CAN, args = (q,))
    th2 = Thread(target = Input_CAN, args = (q,))

    th1.start()
    # th1.join()
    th2.start()
    # th2.join()
             
if __name__ == "__main__":
    
    python_can = PythontoTest()

    # # q = queue.Queue()

    # th1 = Thread(target = python_can.Send_CAN, args = (q,))
    # th2 = Thread(target = python_can.Input_CAN, args = (q,))

    # th1.start()
    # # th1.join()
    # th2.start()
    # # th2.join()