#!/usr/bin/env python
import can
import time
import cantools
from can.message import Message

db = cantools.db.load_file('D:/DCU15_IG/DB/GN7_M/ECANFD_GN7_M.0.dbc')

speed = 100

msg = db.get_message_by_name('CLU_01_20ms')
msg_data = msg.encode({'CLU_DisSpdVal':speed, 'CLU_DisSpdDcmlVal':0, 'CLU_SpdUnitTyp':0, 'CLU_AlvCnt1Val':0, 'CLU_Crc1Val':65535})
# msg_data = db.encode_message('CLU_01_20ms', {'CLU_DisSpdVal':speed, 'CLU_DisSpdDcmlVal':0, 'CLU_SpdUnitTyp':0, 'CLU_AlvCnt1Val':0, 'CLU_Crc1Val':65535})

bus = can.interface.Bus(bustype = 'vector', channel = 0)
msg = can.Message(arbitration_id = msg.frame_id, data = msg_data, is_fd = True, is_extended_id = False)

while(1):
    try:
        bus.send(msg)
        print(msg_data)
        time.sleep(0.01)
    except can.CanError:
        print("Message NOT sent")