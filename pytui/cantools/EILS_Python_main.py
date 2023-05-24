#!/usr/bin/env python
from EILS_Python_CAN import *
import cantools
from can.message import Message
from threading import *
from tkinter import *
import tkinter
import numpy as np
import pandas as pd
import json
from decimal import Decimal

if __name__ == '__main__':
    dir = 'D:\PythonEILS\Data\HKMC\MX5' # 차종에 따라 경로 설정
    
    with open(dir + '\\' + 'config.json', 'r') as f: # JSON 설정 불러오기
        json_data = json.load(f)
        
    dbc_data = json_data['dbc']
    db = cantools.db.load_file(dir + '\\' + dbc_data) # DBC 설정
        
    scenario_data = json_data['scenario']
    df = pd.read_excel(dir + '\\' + scenario_data, sheet_name = None) # 시나리오 설정
    
    scenarioMessages = list(df.keys())
    cyclicMessages = json_data['cyclicMessages']
    eventMessages = json_data['eventMessages']
            
    def scenarioDecision(): # Excel 파일의 시나리오를 읽음
        try:
            for i in range(len(df[scenarioMessages[0]].index)):
                
                while(scenario_pause == 1):
                    time.sleep(0.01)
                    if (scenario_pause != 1):
                        break
                
                for k in range(len(scenarioMessages)):
                    scenario_msg = db.get_message_by_name(scenarioMessages[k])
                    scenarioData_msgData = scenario_msg.encode({scenario_msg.signal_tree[j]:float(df[scenarioMessages[k]].iloc[i + 1, j + 1]) for j in reversed(range(len(scenario_msg.signal_tree)))})
                    canTx.scenarioMessage(scenario_msg, scenarioData_msgData)
                
                time.sleep(df[scenarioMessages[0]]['time'][i + 1] - df[scenarioMessages[0]]['time'][i]) # 시간간격에 따라 실행
                # time.sleep(0.01)
        except:
            canTx.exitThread() # 시나리오 끝나면 종료
            
    def cyclicDefault(): # Cyclic으로 Tx하는 Message의 기본값
        global cyclic_default, cyclic_dict
        cyclic_dict = dict()
        
        for i in range(len(cyclicMessages)):
            cyclic_default = db.get_message_by_name(cyclicMessages[i])

            globals()['cyclic_list' + str(i)] = list()
            cyclic_dict[cyclic_default] = globals()['cyclic_list' + str(i)]
            
            for k in range(len(cyclic_default.signal_tree)):
                if (str(cyclic_default.signals[k].initial) == "None"):
                    globals()['cyclic_list' + str(i)].append(str(cyclic_default.signals[k].offset))
                else:
                    globals()['cyclic_list' + str(i)].append(str(round(((cyclic_default.signals[k].initial) * Decimal(cyclic_default.signals[k].scale) + cyclic_default.signals[k].offset), 4)))
            
    def cyclicDecision(message, signal, value): # Cyclic으로 Tx하는 Message의 변경
        global cyclic_msg, cyclic_msgData
        
        cyclic_msg = db.get_message_by_name(message)

        for i in range(len(cyclic_msg.signal_tree)):
            if (signal == cyclic_msg.signal_tree[i]):
                cyclic_dict[cyclic_msg][i] = value
                cyclic_msgData = cyclic_msg.encode({cyclic_msg.signal_tree[j]:float(cyclic_dict[cyclic_msg][j]) for j in reversed(range(len(cyclic_msg.signal_tree)))})
    
    def eventDefault(): # Event로 Tx하는 Message의 기본값
        global event_default, event_dict
        event_dict = dict()
        
        for i in range(len(eventMessages)):
            event_default = db.get_message_by_name(eventMessages[i])
            globals()['event_list' + str(i)] = list()
            event_dict[event_default] = globals()['event_list' + str(i)]
            
            for k in range(len(event_default.signal_tree)):
                if (str(event_default.signals[k].initial) == "None"):
                    globals()['event_list' + str(i)].append(str(event_default.signals[k].offset))
                else:
                    globals()['event_list' + str(i)].append(str(round(((event_default.signals[k].initial) * Decimal(event_default.signals[k].scale) + event_default.signals[k].offset), 4)))         
        
    def eventDecision(message, signal, value): # Event로 Tx하는 Message의 변경
        global event_msg, event_msgData
        
        event_msg = db.get_message_by_name(message)

        for i in range(len(event_msg.signal_tree)):
            if (signal == event_msg.signal_tree[i]):
                event_dict[event_msg][i] = value
                event_msgData = event_msg.encode({event_msg.signal_tree[j]:float(event_dict[event_msg][j]) for j in reversed(range(len(event_msg.signal_tree)))})
        
    def scenario_start_stop(): #  scenarioMessages 실행 및 정지
        global scenario_pause
        scenario_pause = scenario_pause*(-1)
        
        if (scenario_pause == 1):
            canTx.scenarioStop()
        else:
            canTx.scenarioPlay()
            
    def cyclic_start_stop(): # cyclicMessages 실행 및 정지
        global cyclic_pause
        cyclic_pause = cyclic_pause*(-1)
        error = 0
        
        if (cyclic_pause == 1):
            canTx.CyclicStop()
        else:
            canTx.cyclicPlay()
            for j in range(len(cyclicMessages)):
                if (globals()['checkbtnVar_cyclic' + str(j)].get() != "NONE"):
                    
                    try:
                        error = 0
                        for i in range(len(json_data[globals()['checkbtnVar_cyclic' + str(j)].get()])):
                            
                            check_cyclic_msg = db.get_message_by_name(globals()['checkbtnVar_cyclic' + str(j)].get())
                            length = check_cyclic_msg.get_signal_by_name(json_data[globals()['checkbtnVar_cyclic' + str(j)].get()][i]).length
                            maximum = 2**length - 1 # Value 최대값
                            
                            input_value = globals()['total_cyclic' + str(j)] + i
                            globals()['entry_cyclic_value' + str(input_value)] = float(globals()['entry_cyclic' + str(input_value)].get())
                            
                            if (globals()['entry_cyclic_value' + str(input_value)] > maximum):
                                print("Invalid Value : " + cyclicMessages[j])
                                error = 1
                            else:
                                cyclicDecision(globals()['checkbtnVar_cyclic' + str(j)].get(), json_data[globals()['checkbtnVar_cyclic' + str(j)].get()][i], globals()['entry_cyclic_value' + str(input_value)])
                                
                        if (error == 0): 
                            canTx.cyclicMessage(cyclic_msg, cyclic_msgData)
                            
                    except KeyError:
                        print("Check JSON " + cyclicMessages[j] + " Signal")
                    except:
                        print("Fill Up Value : " + cyclicMessages[j])
    
    def event_start(): # EventMessages 실행
        error = 0
        
        for j in range(len(eventMessages)):
            if (globals()['checkbtnVar_event' + str(j)].get() != "NONE"):
                
                try:
                    error = 0
                    for i in range(len(json_data[globals()['checkbtnVar_event' + str(j)].get()])):
                        
                        check_event_msg = db.get_message_by_name(globals()['checkbtnVar_event' + str(j)].get())
                        length = check_event_msg.get_signal_by_name(json_data[globals()['checkbtnVar_event' + str(j)].get()][i]).length
                        maximum = 2**length - 1 # Value 최대값
                        
                        input_value = globals()['total_event' + str(j)] + i
                        globals()['entry_event_value' + str(input_value)] = float(globals()['entry_event' + str(input_value)].get())
                        
                        if (globals()['entry_event_value' + str(input_value)] > maximum):
                            print("Invalid Value : " + eventMessages[j])
                            error = 1
                        else:
                            eventDecision(globals()['checkbtnVar_event' + str(j)].get(), json_data[globals()['checkbtnVar_event' + str(j)].get()][i], globals()['entry_event_value' + str(input_value)])
                            
                    if (error == 0):        
                        canTx.eventMessage(event_msg, event_msgData)
                        canTx.eventTransmit()
                except KeyError:
                    print("Check JSON " + eventMessages[j] + " Signal")
                except:
                    print("Fill Up Value : " + eventMessages[j])
   
    def numEventsignalList(): # Event로 Tx하는 Signal의 위치 결정
        global num_Eventsignal_list
        num_Eventsignal_list = list()
        
        try:
            for j in range(len(eventMessages)):
                globals()['total_event' + str(j)] = 0
                
                if (j != 0):
                    globals()['total_event' + str(j)] = len(json_data[eventMessages[j - 1]]) + globals()['total_event' + str(j - 1)]
                    
                num_Eventsignal_list.append(globals()['total_event' + str(j)])
        except KeyError:
            print("Check JSON eventMessages")
        
    def EventsignalList(): # Event로 Tx하는 Signal의 List
        global Eventsignal_list
        Eventsignal_list = list()    
        for q in range(len(eventMessages)):
            
            for w in range(len(json_data[eventMessages[q]])):
                Eventsignal_list.append(json_data[eventMessages[q]][w])
                
    def numCyclicsignalList(): # Cyclic으로 Tx하는 Signal의 위치 결정
        global num_Cyclicsignal_list
        num_Cyclicsignal_list = list()
        
        try:
            for j in range(len(cyclicMessages)):
                globals()['total_cyclic' + str(j)] = 0
                
                if (j != 0):
                    globals()['total_cyclic' + str(j)] = len(json_data[cyclicMessages[j - 1]]) + globals()['total_cyclic' + str(j - 1)]
                    
                num_Cyclicsignal_list.append(globals()['total_cyclic' + str(j)])
        except KeyError:
            print("Check JSON cyclicMessages")
        
    def CyclicsignalList(): # Cyclic으로 Tx하는 Signal의 List
        global Cyclicsignal_list
        Cyclicsignal_list = list()    
        for q in range(len(cyclicMessages)):
            
            for w in range(len(json_data[cyclicMessages[q]])):
                Cyclicsignal_list.append(json_data[cyclicMessages[q]][w])
            
    def GUI(): # GUI로 CAN Tx
        
        tk = Tk()
        tk.title('CAN Test (Input Physical Value)')
        tk.minsize(width = 900, height = 600)
        tk.maxsize(width = 900, height = 600)

        scenario_btn = Button(tk, text = 'Scenario start/stop', command = scenario_start_stop)
        event_btn = Button(tk, text = "Event start", command = event_start)
        cyclic_btn = Button(tk, text = "Cyclic start/stop", command = cyclic_start_stop)
        scenario_btn.place(x = 10, y = 10)
        event_btn.place(x = 150, y = 10)
        cyclic_btn.place(x = 600, y = 10)
        
        y_height_1 = 56
        y_height_2 = 60
        y_height_3 = 56
        y_height_4 = 60
        
        for i in range(len(eventMessages)): # EventMessage Checkbutton 만들기
            wid = 25

            if (i != 0):
                y_height_1 += (wid*(num_Eventsignal_list[i] - num_Eventsignal_list[i-1]) + 25)
            
            globals()['checkbtnVar_event' + str(i)] = tkinter.StringVar()
            check_btn_event = Checkbutton(tk, text = eventMessages[i], variable = globals()['checkbtnVar_event' + str(i)], onvalue = eventMessages[i], offvalue = "NONE")
            check_btn_event.place(x = 10, y = y_height_1)
            check_btn_event.deselect()
        
        for i in range(len(Eventsignal_list)): # EventMessage Entry/Label 만들기
            if (i in num_Eventsignal_list):
                wid = 25
            else:
                wid = 0

            if (i != 0):
                y_height_2 += (wid + 25)
                
            globals()['entry_event' + str(i)] = Entry(tk)
            globals()['entry_event' + str(i)].place(x = 180, y = y_height_2, width = 60)
            label_signals = Label(tk, text = Eventsignal_list[i])
            label_signals.place(x = 250, y = y_height_2)
            
        for i in range(len(cyclicMessages)): # CyclicMessage Checkbutton 만들기
            wid = 25

            if (i != 0):
                y_height_3 += (wid*(num_Cyclicsignal_list[i] - num_Cyclicsignal_list[i-1]) + 25)
            
            globals()['checkbtnVar_cyclic' + str(i)] = tkinter.StringVar()
            check_btn_cyclic = Checkbutton(tk, text = cyclicMessages[i], variable = globals()['checkbtnVar_cyclic' + str(i)], onvalue = cyclicMessages[i], offvalue = "NONE")
            check_btn_cyclic.place(x = 460, y = y_height_3)
            check_btn_cyclic.deselect()
            
        for i in range(len(Cyclicsignal_list)): # CyclicMessage Entry/Label 만들기
            if (i in num_Cyclicsignal_list):
                wid = 25
            else:
                wid = 0

            if (i != 0):
                y_height_4 += (wid + 25)
                
            globals()['entry_cyclic' + str(i)] = Entry(tk)
            globals()['entry_cyclic' + str(i)].place(x = 630, y = y_height_4, width = 60)
            label_signals = Label(tk, text = Cyclicsignal_list[i])
            label_signals.place(x = 700, y = y_height_4)
                    
        tk.mainloop()
        
    thread_GUI = Thread(target = GUI, args = ())
    thread_GUI.start()
    
    while(1): # 실행값
        numEventsignalList()
        EventsignalList()
        numCyclicsignalList()
        CyclicsignalList()
        
        canTx = CanTransmit(1)
        
        eventDefault()
        cyclicDefault()
        
        scenario_pause = -1
        scenario_start_stop()
        cyclic_pause = -1
        cyclic_start_stop()
          
        scenarioDecision()