#!/usr/bin/env python
from can_json import *
import cantools
import can
from can.message import Message
from threading import *
from tkinter import *
import numpy as np
import pandas as pd
import json

if __name__ == '__main__':
    db = cantools.db.load_file('D:/DCU15_IG/DB/GN7_M/ECANFD_GN7_M.0.dbc') # DBC 설정
    df = pd.read_excel('D:\GIT\cantools\cantools\data.xlsx', sheet_name = 'Sheet1') # 시나리오 설정
    
    with open('D:\DCU15_IG\DB\GN7_M\\ECANFD_GN7_M.0.json', 'r') as f:
        json_data = json.load(f)
        
    periodMessages = json_data['periodMessages']
    eventMessages = json_data['eventMessages']
    
    def periodDecision(message, signal, value): # excel파일의 시나리오를 읽음
        global period_msg, period_msgData
        
        period_msg = db.get_message_by_name(message)

        for i in range(len(period_msg.signal_tree)):
            if (signal == period_msg.signal_tree[i]):
                period_dict[period_msg][i] = value
                period_msgData = period_msg.encode({period_msg.signal_tree[j]:int(period_dict[period_msg][j]) for j in reversed(range(len(period_msg.signal_tree)))})
                
    def periodDefault(): # json파일을 읽고 initial value Tx
        global period_default, canTx_dict, period_dict
        canTx_dict = dict()
        period_dict = dict()
        
        for i in range(len(periodMessages)):
            period_default = db.get_message_by_name(periodMessages[i])
            msgData_default = period_default.encode({period_default.signal_tree[j]:int(period_default.signals[j].initial) for j in reversed(range(len(period_default.signal_tree)))})
                
            globals()['canTx' + str(i)] = CanTransmit(1)
            globals()['canTx' + str(i)].periodMessage(period_default, msgData_default, period_default.cycle_time) # int(periodMessages[i].split('_')[-1].split('m')[0])
            canTx_dict[period_default] = globals()['canTx' + str(i)]
            globals()['period_list' + str(i)] = list()
            period_dict[period_default] = globals()['period_list' + str(i)]
            
            for k in range(len(period_default.signal_tree)):
                globals()['period_list' + str(i)].append(str(period_default.signals[k].initial))
                
    def eventDefault():
        global event_default, event_dict
        event_dict = dict()
        
        for i in range(len(eventMessages)):
            event_default = db.get_message_by_name(eventMessages[i])
            globals()['manual_list' + str(i)] = list()
            event_dict[event_default] = globals()['manual_list' + str(i)]
            
            for k in range(len(event_default.signal_tree)):
                globals()['manual_list' + str(i)].append(str(event_default.signals[k].initial))
            
    def eventDecision(message, signal, value):
        global event_msg, event_msgData
        
        event_msg = db.get_message_by_name(message)

        for i in range(len(event_msg.signal_tree)):
            if (signal == event_msg.signal_tree[i]):
                event_dict[event_msg][i] = value
                event_msgData = event_msg.encode({event_msg.signal_tree[j]:int(event_dict[event_msg][j]) for j in reversed(range(len(event_msg.signal_tree)))})
    
    pause = 1
    
    def can_start():
        global pause
        pause = 0
        for k in range(len(periodMessages)):
            globals()['canTx' + str(k)].start()

    def can_stop():
        global pause
        pause = 1
        for k in range(len(periodMessages)):
            globals()['canTx' + str(k)].stop()
            
    def event1():
        eventDecision('HU_CLU_PE_05', 'HU_NaviStatus', 2)
        canTx0.eventMessage(event_msg, event_msgData)
        eventDecision('HU_GW_PE_01', 'HU_AliveStatus', 3)
        canTx0.eventMessage(event_msg, event_msgData)
        
        canTx0.eventTransmit()
        
    def event2():
        eventDecision('HU_MON_PE_01', 'HU_AdasSupport', 2)
        canTx0.eventMessage(event_msg, event_msgData)
        
        canTx0.eventTransmit()
        
    def GUI():
        
        tk = Tk()
        tk.title('CAN Test')
        tk.minsize(width = 200, height = 200)
        tk.maxsize(width = 200, height = 200)

        btn_can1 = Button(tk, text = 'can_start', command = can_start)
        btn_can2 = Button(tk, text = 'can_stop', command = can_stop)
        btn_can3 = Button(tk, text = 'event1', command = event1)
        btn_can4 = Button(tk, text = 'event2', command = event2)
        
                    
        btn_can1.place(x = 73, y = 45)
        btn_can2.place(x = 73, y = 88)
        btn_can3.place(x = 73, y = 130)
        btn_can4.place(x = 73, y = 170)
                    
        tk.mainloop()
    
    thread_GUI = Thread(target = GUI, args = ())
    thread_GUI.start()
    
    while(1):
        periodDefault()
        eventDefault()
        can_stop()
        
        for i in range(len(df.index)):
                
            while(pause):
                time.sleep(0.1)
                if (pause != 1):
                    break
            
            periodDecision(df.loc[i, 'message'], df.loc[i, 'signal'], df.loc[i, 'value']) # excel 정보를 읽어옴
               
            canTx_dict[period_msg].periodMessage(period_msg, period_msgData, period_msg.cycle_time) # excel에서 읽어온 정보를 업데이트
                        
            try:
                time.sleep(df.loc[i + 1,'time'] - df.loc[i,'time']) # 시간간격에 따라 실행
            except:
                for k in range(len(periodMessages)): # 시나리오 끝나면 종료
                    globals()['canTx' + str(k)].terminate()