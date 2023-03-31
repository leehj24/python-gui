#!/usr/bin/env python
from canTxRx3 import *
import cantools
from can.message import Message
from threading import*
from tkinter import *
import numpy as np
import pandas as pd

if __name__ == '__main__':
    db = cantools.db.load_file('D:/DCU15_IG/DB/GN7_M/ECANFD_GN7_M.0.dbc') # DBC 설정
    df = pd.read_excel('D:\GIT\cantools\cantools\data.xlsx', sheet_name = 'default') # 초기값 설정
    df1 = pd.read_excel('D:\GIT\cantools\cantools\data.xlsx', sheet_name = 'Sheet3') # 시나리오 설정
    
    def periodSpilt(): # excel의 메세지의 주기를 저장
        global period_list
        period_list = list()
        
        for i in range(len(df1.index)):
            period = int(df1.loc[i, 'message'].split('_')[-1].split('m')[0])
            period_list.append(period)
    
    def msgDecision(message, signal, value): # 시나리오를 읽음
        global msg, msgData
        msg = db.get_message_by_name(message)
        
        for i in range(len(msg.signal_tree)):
            if (signal == msg.signal_tree[i]):
                df.loc[i, message] = value
                msgData = msg.encode({msg.signal_tree[j]:int(df.loc[j, message]) for j in reversed(range(len(msg.signal_tree)))})
                
    def sendDefault(): # default 시트를 읽고 자동으로 출력
        global msg_default, canTx_dict
        canTx_dict = dict()
        df = pd.read_excel('D:\GIT\cantools\cantools\data.xlsx', sheet_name = 'default')
        
        for i in range(len(df.columns)):
            msg_default = db.get_message_by_name(df.columns[i])
            msgData_default = msg_default.encode({msg_default.signal_tree[j]:int(df.loc[j, df.columns[i]]) for j in reversed(range(len(msg_default.signal_tree)))})
            
            globals()['canTx' + str(i)] = CanTransmit(1,condition_obj)
            globals()['canTx' + str(i)].updateMessage(msg_default, msgData_default, int(df.columns[i].split('_')[-1].split('m')[0]))
            canTx_dict[msg_default] = globals()['canTx' + str(i)]
            
    pause = 0
    
    def can_start():
        global pause
        pause = 1
        print(pause)
                    
    def can_stop():
        global pause
        pause = 0
        print(pause)
        
    def GUI():
        
        tk = Tk()
        tk.title('CAN Test')
        tk.minsize(width = 200, height = 200)
        tk.maxsize(width = 200, height = 200)

        btn_can1 = Button(tk, text = 'can_start', command = can_start)
        btn_can2 = Button(tk, text = 'can_stop', command = can_stop)
                    
        btn_can1.place(x = 73, y = 45)
        btn_can2.place(x = 73, y = 110)
                    
        tk.mainloop()
    
    thread1 = Thread(target = GUI, args = ())
    thread1.start()
    
    while(1):
        for i in range(len(df1.index)):
            condition_obj.acquire()
                    
            if (i == 0): # 처음에만 실행
                periodSpilt()
                sendDefault()
                print('Default')
                print(pause)
                
            if (pause == 0):
                while(pause != 1):
                    for k in range(len(df.columns)):
                        globals()['canTx' + str(k)].stop()
                    if (pause == 1):
                        for k in range(len(df.columns)):
                            globals()['canTx' + str(k)].start()
                        break
            
            msgDecision(df1.loc[i, 'message'], df1.loc[i, 'signal'], df1.loc[i, 'value']) # excel 정보를 읽어옴
                    
            canTx_dict[msg].updateMessage(msg, msgData, period_list[i]) # excel에서 읽어온 정보를 업데이트
                        
            if (i != len(df1.index) - 1):
                condition_obj.wait(df1.loc[i + 1,'time'] - df1.loc[i,'time']) # 시간간격에 따라 실행
            else:
                print("End")
                for k in range(len(df.columns)): # 시나리오 끝나면 종료
                    globals()['canTx' + str(k)].terminate()