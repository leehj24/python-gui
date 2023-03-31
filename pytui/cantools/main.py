#!/usr/bin/env python
from canteam import *
import can
import cantools
from can.message import Message
from threading import*
import queue
import time
from tkinter import *

if __name__ == '__main__':
    db = cantools.db.load_file('D:/DCU15_IG/DB/GN7_M/ECANFD_GN7_M.0.dbc')

    msg1 = db.get_message_by_name('CLU_01_20ms')
    msgData1 = msg1.encode({'CLU_DisSpdVal':0, 'CLU_DisSpdDcmlVal':0, 'CLU_SpdUnitTyp':0, 'CLU_AlvCnt1Val':0, 'CLU_Crc1Val':65535})

    msg2 = db.get_message_by_name('CLU_02_100ms')
    msgData2 = msg2.encode({'CLU_DrvngModSwSta':1, 'CLU_OdoVal':0.0, 'CLU_AlvCnt2Val':0, 'CLU_Crc2Val':65535})

    canTx1 = CanTransmit(1, msg1, msgData1)
    canTx1.registerMessage(msg1, msgData1)
    canTx1.updateMessage(msg1, msgData1)
    
    canTx2 = CanTransmit(1, msg2, msgData2)
    canTx2.registerMessage(msg2, msgData2)
    canTx2.updateMessage(msg2, msgData2)