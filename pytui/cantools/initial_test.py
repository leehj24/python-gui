#!/usr/bin/env python
from can_json import *
import cantools
import can
from can.message import Message
from threading import*
import json

db = cantools.db.load_file('D:/DCU15_IG/DB/GN7_M/ECANFD_GN7_M.0.dbc') # DBC 설정

with open('D:\DCU15_IG\DB\GN7_M\\ECANFD_GN7_M.0.json', 'r') as f:
    json_data = json.load(f)

periodMessages = json_data['periodMessages']
manualMessages = json_data['manualMessages']
print(periodMessages)
print(manualMessages)

# dbc = dict()
# for i in range(len(periodMessages)):
#     msg = db.get_message_by_name(periodMessages[i])
    
#     for j in range(len(msg.signals)):
#         dbc[msg.signals[j].name] = msg.signals[j].initial
        
#     print(dbc)
    

def sendDefault(): # json파일을 읽고 initial value Tx
    global msg_default, canTx_dict
    canTx_dict = dict()
    value_list = list()
    
    for i in range(len(periodMessages)):
        msg_default = db.get_message_by_name(periodMessages[i])
        msgData_default = msg_default.encode({msg_default.signal_tree[j]:int(msg_default.signals[j].initial) for j in reversed(range(len(msg_default.signal_tree)))})

        for k in range(len(msg_default.signal_tree)):
            value_list.append(int(msg_default.signals[k].initial))
        
        for i in range(len(periodMessages)):
            globals()['value_list' + str(i)] = list()
            
            for j in range(len(msg_default.signal_tree)):
                globals()['value_list' + str(i)].append(str(msg_default.signals[j].initial))
            
            print(globals()['value_list' + str(i)]) # append로 쌓아야함
            
        # globals()['canTx' + str(i)] = CanTransmit(1)
        # globals()['canTx' + str(i)].updateMessage(msg_default, msgData_default, int(periodMessages[i].split('_')[-1].split('m')[0]))
        # canTx_dict[msg_default] = globals()['canTx' + str(i)]
        
sendDefault()