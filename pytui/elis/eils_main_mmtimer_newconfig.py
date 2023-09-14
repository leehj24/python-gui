#!/usr/bin/env python
import cantools
import tkinter
import pandas as pd
import json
from decimal import Decimal
from eils_can_mmtimer import *
from eils_mmtimer import *
from threading import *
from tkinter import *

class guiSetting:
    def __init__(self, cyclicMessages, eventMessages):
        self.total_cyclic = [0 for _ in range(len(cyclicMessages))]     # cyclic message마다 signal의 시작점 숫자의 list
        self.cyclicsignal_list = list()                                 # cyclic signal label들의 list
        self.cyclicMessages = cyclicMessages                            # cyclic message들의 list
        
        self.total_event = [0 for _ in range(len(eventMessages))]       # event message마다 signal의 시작점 숫자의 list
        self.eventsignal_list = list()                                  # event signal label들의 list
        self.eventMessages = eventMessages                              # event message들의 list

    def numCyclicsignalList(self):
        try:
            for j in range(len(self.cyclicMessages)):
                if (j != 0):
                    self.total_cyclic[j] = len(json_data[self.cyclicMessages[j - 1]]) + self.total_cyclic[j - 1]

        except KeyError:
            print("Check JSON cyclicMessages")
            
        return self.total_cyclic

    def CyclicsignalList(self):
        for q in range(len(self.cyclicMessages)):
            
            for w in range(len(json_data[self.cyclicMessages[q]])):
                self.cyclicsignal_list.append(json_data[self.cyclicMessages[q]][w])
                
        return self.cyclicsignal_list
    
    def numEventsignalList(self):
        try:
            for j in range(len(self.eventMessages)):
                if (j != 0):
                    self.total_event[j] = len(json_data[self.eventMessages[j - 1]]) + self.total_event[j - 1]
                    
        except KeyError:
            print("Check JSON eventMessages")
            
        return self.total_event
    
    def EventsignalList(self):  
        for q in range(len(self.eventMessages)):
            
            for w in range(len(json_data[self.eventMessages[q]])):
                self.eventsignal_list.append(json_data[self.eventMessages[q]][w])
                
        return self.eventsignal_list

class guiEILS:
    def __init__(self, eventMessages, cyclicMessages, total_event, eventsignal_list, total_cyclic, cyclicsignal_list):
        self.checkbtnVar_event = list()                                 # event checkbox 상태
        self.checkbtnVar_cyclic = list()                                # cyclic checkbox 상태
        self.entry_event = list()                                       # event entry에 적힌 값
        self.entry_cyclic = list()                                      # cyclic entry에 적힌 값
        
        self.eventMessages = eventMessages                              # event message들의 list
        self.cyclicMessages = cyclicMessages                            # cyclic message들의 list
        
        self.total_event = total_event                                  # event message마다 signal의 시작점 숫자의 list
        self.eventsignal_list = eventsignal_list                        # event message 개수
        self.total_cyclic = total_cyclic                                # cyclic message마다 signal의 시작점 숫자의 list
        self.cyclicsignal_list = cyclicsignal_list                      # cyclic message 개수
        
    def gui(self):
        tk = Tk()
        tk.title('CAN Test (Input Physical Value)')
        tk.minsize(width = 950, height = 700)
        tk.maxsize(width = 950, height = 700)

        scenario_btn = Button(tk, text = 'Scenario start/stop', command = scenario.startAndstop)
        event_btn = Button(tk, text = "Event start", command = event.start)
        cyclic_start_btn = Button(tk, text = "Cyclic start", command = cyclic.start)
        cyclic_stop_btn = Button(tk, text = "Cyclic stop", command = cyclic.stop)
        scenario_btn.place(x = 10, y = 10)
        event_btn.place(x = 150, y = 10)
        cyclic_start_btn.place(x = 460, y = 10)
        cyclic_stop_btn.place(x = 550, y = 10)
        
        y_height_1 = 56
        y_height_2 = 60
        y_height_3 = 56
        y_height_4 = 60
        
        for i in range(len(self.eventMessages)): # EventMessage Checkbutton 만들기
            wid = 25

            if (i != 0):
                y_height_1 += (wid*(self.total_event[i] - self.total_event[i-1]) + 25)
            
            self.checkbtnVar_event.append(tkinter.StringVar())
            check_btn_event = Checkbutton(tk, text = self.eventMessages[i], variable = self.checkbtnVar_event[i], onvalue = self.eventMessages[i], offvalue = "NONE")
            check_btn_event.place(x = 10, y = y_height_1)
            check_btn_event.deselect()
        
        for i in range(len(self.eventsignal_list)): # EventMessage Entry/Label 만들기
            if (i in self.total_event):
                wid = 25
            else:
                wid = 0

            if (i != 0):
                y_height_2 += (wid + 25)
                
            self.entry_event.append(Entry(tk))
            self.entry_event[i].place(x = 180, y = y_height_2, width = 60)
            label_signals = Label(tk, text = self.eventsignal_list[i])
            label_signals.place(x = 250, y = y_height_2)
            
        for i in range(len(self.cyclicMessages)): # CyclicMessage Checkbutton 만들기
            wid = 25

            if (i != 0):
                y_height_3 += (wid*(self.total_cyclic[i] - self.total_cyclic[i-1]) + 25)
            
            self.checkbtnVar_cyclic.append(tkinter.StringVar())
            check_btn_cyclic = Checkbutton(tk, text = self.cyclicMessages[i], variable = self.checkbtnVar_cyclic[i], onvalue = self.cyclicMessages[i], offvalue = "NONE")
            check_btn_cyclic.place(x = 460, y = y_height_3)
            check_btn_cyclic.deselect()
            
        for i in range(len(self.cyclicsignal_list)): # CyclicMessage Entry/Label 만들기
            if (i in self.total_cyclic):
                wid = 25
            else:
                wid = 0

            if (i != 0):
                y_height_4 += (wid + 25)
                
            self.entry_cyclic.append(Entry(tk))
            self.entry_cyclic[i].place(x = 650, y = y_height_4, width = 60)
            label_signals = Label(tk, text = self.cyclicsignal_list[i])
            label_signals.place(x = 720, y = y_height_4)
                    
        tk.mainloop()
        
    def returnParameter(self):
        return self.checkbtnVar_event, self.checkbtnVar_cyclic, self.entry_event, self.entry_cyclic

class scenarioCAN:
    def __init__(self, scenarioMessages):
        self.scenarioMessages = scenarioMessages                        # scenario message들의 list
        self.mappingMessages = mappingMessages                          # mapping된 message/signal 집합
        self.error = 0                                                  # error 여부
        self.scenario_index = 0                                         # scenario time
        self.play = False                                               # scenario start/stop
        self.scenario_dict = dict()                                     # msg data를 만들 scenario dict
        self.checkDB = dict()                                           # scenario message의 db, ch, cycle_time 설정
        
        for msgName in self.scenarioMessages:
            for dbc in db:
                if msgName in dbc._name_to_message.keys():
                    msg = dbc.get_message_by_name(msgName)
                    cycle_time = msg.cycle_time
                    ch = db.index(dbc)
                    self.checkDB[msgName] = [dbc, ch, cycle_time]
        
        for mappingName in self.mappingMessages:
            print(mapping_data[mappingName])
        
        self.setting()
    
    def setting(self):
        for msgName, valueDict in self.checkDB.items():
            scenarioValues = list()
            dbc = valueDict[0]
            scenarioDefault = dbc.get_message_by_name(msgName)
            
            for signal in scenarioDefault.signals:
                if (str(signal.initial) == "None"):
                    scenarioValues.append(str(signal.offset))
                else:
                    scenarioValues.append(str(round((signal.initial * Decimal(signal.scale) + Decimal(signal.offset)), 4)))
                    
            self.scenario_dict[scenarioDefault] = scenarioValues
    
    def scenario(self):
        if self.play == True:
            for mappingName in self.mappingMessages:
                for msgName, sigName in mapping_data[mappingName].items():
                    dbc, ch, cycleTime = self.checkDB[msgName]
                    msg = dbc.get_message_by_name(msgName)
                    
                    for i in range(len(msg.signal_tree)):
                        if (sigName == msg.signal_tree[i]):
                            self.scenario_dict[msg][i] = df[mappingName].iloc[self.scenario_index]
                            msgData = msg.encode({msg.signal_tree[j]:float(self.scenario_dict[msg][j]) for j in reversed(range(len(msg.signal_tree)))})
                        
                    canTx.scenarioMessage(ch, cycleTime, msg, msgData)
                    
            canTx.scenarioTransmit(self.scenario_index)
            
            if self.scenario_index >= len(df.index) - 1:
                self.scenario_index = len(df.index) - 1
            else:
                self.scenario_index += 1
    
    def startAndstop(self):
        if (self.play == False):
            self.play = True
            if (self.scenario_index == len(df.index) - 1):
                self.scenario_index = 0
        else:
            self.play = False
        
        if (self.play == False):
            canTx.scenarioStop()
        else:
            canTx.scenarioPlay()

class cyclicCAN:
    def __init__(self, cyclicMessages):
        self.cyclicMessages = cyclicMessages                            # cyclic message들의 list
        self.error = 0                                                  # error 여부
        self.cyclic_dict = dict()                                       # msg data를 만들 cyclic dict
        self.checkDB = dict()                                           # cyclc message의 db, ch, cycle_time 설정
        
        for msgName in self.cyclicMessages:
            for dbc in db:
                if msgName in dbc._name_to_message.keys():
                    msg = dbc.get_message_by_name(msgName)
                    cycle_time = msg.cycle_time
                    ch = db.index(dbc)
                    self.checkDB[msgName] = [dbc, ch, cycle_time]
                    
        self.setting()

    def setting(self):
        for msgName, valueDict in self.checkDB.items():
            cyclicValues = list()
            dbc = valueDict[0]
            cyclic_default = dbc.get_message_by_name(msgName)
            
            for signal in cyclic_default.signals:
                if (str(signal.initial) == "None"):
                    cyclicValues.append(str(signal.offset))
                else:
                    cyclicValues.append(str(round((signal.initial * Decimal(signal.scale) + Decimal(signal.offset)), 4)))
                    
            self.cyclic_dict[cyclic_default] = cyclicValues

    def start(self):
        canTx.cyclicPlay()
        updateMsg = {"VCU_01_10ms" : {"VCU_GearPosSta" : 6},
                     "WHL_01_10ms" : {"WHL_SpdFLVal" : 1.0, "WHL_SpdFRVal" : 1.1}, 
                     "SAS_01_10ms" : {"SAS_AnglVal" : 0}, 
                     "A_FR_C_RDR_Obj_01_50ms" : {"FR_C_RDR_Obj_ID01Val" : 3}}
        
        for msgName, sigDict in updateMsg.items():
            dbc, ch, cycleTime = self.checkDB[msgName]
            
            for sigName, sigValue in sigDict.items():
                msg = dbc.get_message_by_name(msgName)
                for i in range(len(msg.signal_tree)):
                    if (sigName == msg.signal_tree[i]):
                        self.cyclic_dict[msg][i] = sigValue
                        msgData = msg.encode({msg.signal_tree[j]:float(self.cyclic_dict[msg][j]) for j in reversed(range(len(msg.signal_tree)))})
                    
            canTx.cyclicMessage(ch, cycleTime, msg, msgData)

    def stop(self):
        canTx.CyclicStop()

class eventCAN:
    def __init__(self, eventMessages):
        self.eventMessages = eventMessages                              # event message들의 list
        self.error = 0                                                  # error 여부
        self.event_dict = dict()                                        # msg data를 만들 event dict
        self.checkDB = dict()                                           # event message의 db, ch 설정
        
        for msgName in self.eventMessages:
            for dbc in db:
                if msgName in dbc._name_to_message.keys():
                    ch = db.index(dbc)
                    self.checkDB[msgName] = [dbc, ch]
        
        self.setting()

    def setting(self):
        for msgName, valueDict in self.checkDB.items():
            eventValues = list()
            dbc = valueDict[0]
            event_default = dbc.get_message_by_name(msgName)
            
            for signal in event_default.signals:
                if (str(signal.initial) == "None"):
                    eventValues.append(str(signal.offset))
                else:
                    eventValues.append(str(round((signal.initial * Decimal(signal.scale) + Decimal(signal.offset)), 4)))
                    
            self.event_dict[event_default] = eventValues
    
    def start(self):
        updateMsg = {"CLU_12_00ms" : {"USM_AdasUSMResetReq" : 1.0}, 
                     "CLU_13_00ms" : {"USM_AdasRCCWSetReq" : 1.0}, 
                     "CLU_25_00ms" : {"USM_AdasSEW3SetReq" : 1.0, "USM_AdasSEA3SetReq" : 2.0, "USM_AdasBCA2SetReq" : 1.0, "USM_AdasFCAFrSdSetReq" : 2.0}}
        
        for msgName, sigDict in updateMsg.items():
            dbc, ch = self.checkDB[msgName]
            
            for sigName, sigValue in sigDict.items():
                msg = dbc.get_message_by_name(msgName)
                for i in range(len(msg.signal_tree)):
                    if (sigName == msg.signal_tree[i]):
                        self.event_dict[msg][i] = sigValue
                        msgData = msg.encode({msg.signal_tree[j]:float(self.event_dict[msg][j]) for j in reversed(range(len(msg.signal_tree)))})
                    
            canTx.eventMessage(ch, msg, msgData)
            canTx.eventTransmit()

if __name__ == '__main__':
    # 경로 및 환경 설정
    dir = 'D:\\GIT\\pythonGUI\\Data\\HKMC\\NE1N'
    with open(dir + '\\' + 'config.json', 'r') as f:
        json_data = json.load(f)

    dbc_path = list()
    db = list()
    for i in range(len(json_data['dbc'])):
        dbc_path.append(dir + '\\DB\\' + json_data['dbc'][i])
        db.append(cantools.db.load_file(dbc_path[i]))
    
    scenario_data = json_data['scenario']
    cyclicMessages = json_data['cyclicMessages']
    eventMessages = json_data['eventMessages']
    
    # mapping 설정 json
    dir_mapping = 'D:\\GIT\\pythonGUI\\config'
    with open(dir_mapping + '\\' + 'mapping.json', 'r') as m:
        mapping_data = json.load(m)
        
    df = pd.read_excel(dir + '\\' + scenario_data, sheet_name = 'BCA')
    mappingMessages = list(df.columns)[1:]
    
    scenarioMessages = list()
    for mappingName in mappingMessages:
        msgName = list(mapping_data[mappingName].keys())[0]
        if msgName in scenarioMessages:
            pass
        else:
            scenarioMessages.append(msgName)
    
    # main
    canTx = canTransmit()
    
    setting = guiSetting(cyclicMessages, eventMessages)
    total_event = setting.numEventsignalList()
    eventsignal_list = setting.EventsignalList()
    total_cyclic = setting.numCyclicsignalList()
    cyclicsignal_list = setting.CyclicsignalList()
    
    gui = guiEILS(eventMessages, cyclicMessages, total_event, eventsignal_list, total_cyclic, cyclicsignal_list)
    checkbtnVar_event, checkbtnVar_cyclic, entry_event, entry_cyclic = gui.returnParameter()
    
    cyclic = cyclicCAN(cyclicMessages)
    event = eventCAN(eventMessages)
    scenario = scenarioCAN(scenarioMessages)

    dt = 0.01
    timer = mmtimer(int(dt*1000), scenario.scenario) # inveral = 10ms, resoltion = 0
    timer.start()
    
    gui.gui()