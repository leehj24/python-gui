#!/usr/bin/env python
from canTxRx import *
import can
import cantools
from can.message import Message
from threading import*
from tkinter import *
import numpy as np
import pandas as pd

if __name__ == '__main__':
    db = cantools.db.load_file('D:/DCU15_IG/DB/GN7_M/ECANFD_GN7_M.0.dbc')
    # df = pd.read_excel('D:\GIT\cantools\cantools\data.xlsx', sheet_name = 'data')

    msg1 = db.get_message_by_name('CLU_01_20ms')
    msgData1 = msg1.encode({'CLU_DisSpdVal':100, 'CLU_DisSpdDcmlVal':0, 'CLU_SpdUnitTyp':0, 'CLU_AlvCnt1Val':0, 'CLU_Crc1Val':65535})

    msg2 = db.get_message_by_name('CLU_02_100ms')
    msgData2 = msg2.encode({'CLU_DrvngModSwSta':1, 'CLU_OdoVal':0.0, 'CLU_AlvCnt2Val':0, 'CLU_Crc2Val':65535})
    
    # vel = 0
    # msg3 = db.get_message_by_name('WHL_01_10ms')
    # msgData3 = msg3.encode({'WHL_SpdRRVal':vel, 'WHL_SpdRLVal':vel, 'WHL_SpdFRVal':vel, 'WHL_SpdFLVal':vel, 
    #                         'WHL_PlsRRVal':0, 'WHL_PlsRLVal':0, 'WHL_PlsFRVal':0, 'WHL_PlsFLVal':0, 'WHL_AlvCnt1Val':0, 'WHL_Crc1Val':65535})
    
    canTx1 = CanTransmit(1)
    canTx2 = CanTransmit(1)
    canTx1.updateMessage(msg1, msgData1, 10)
    canTx1.manualMessage(msg1, msgData1)
    # canTx1.manualMessage(msg2, msgData2) # 겹치면 마지막으로 선언한 msgData만 나감
    # canTx1.rampMessage(msg3, msgData3, 0, 200)
    canTx2.updateMessage(msg2, msgData2, 20)
    
    tk = Tk()
    tk.title('CAN Test')
    tk.minsize(width = 200, height = 200)
    tk.maxsize(width = 200, height = 200)
    
    def can_start():
        canTx1.start()
        canTx2.start()
        
    def can_stop():
        canTx1.stop()
        canTx2.stop()
        
    def once_transmit():
        canTx1.onceTransmit()
        # canTx2.onceTransmit()
        
    # def ramp_transmit():
    #     canTx1.rampTransmit()
    #     canTx2.rampTransmit()

    btn_can1 = Button(tk, text = 'can_start', command = can_start)
    btn_can2 = Button(tk, text = 'can_stop', command = can_stop)
    btn_can3 = Button(tk, text = 'manual_msg', command = once_transmit)
    # btn_can4 = Button(tk, text = 'ramp_msg', command = ramp_transmit)
    
    btn_can1.place(x = 60, y = 5)
    btn_can2.place(x = 60, y = 30)
    btn_can3.place(x = 60, y = 55)
    # btn_can4.place(x = 60, y = 80)
    
    tk.mainloop()