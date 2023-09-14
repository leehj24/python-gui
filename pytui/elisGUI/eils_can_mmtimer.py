#!/usr/bin/env python
import can
import queue
from enum import Enum
from eils_mmtimer import *

class CanStatus(Enum):
    STOP = 0
    START = 1
    LIST_CLEAR = 2

class canTransmit:
    def __init__(self):
        self.bus = list()
        for i in range(4):
            self.bus.append(can.interface.Bus(bustype = 'vector', channel = i))

        self.scenarioMessages = dict()
        self.cyclicMessages = dict()
        
        self.scenarioQueue = queue.Queue()
        self.cyclicQueue = queue.Queue()
        self.eventQueue = queue.Queue()
        
        self.scenario_play = CanStatus.STOP
        self.cyclic_play = CanStatus.STOP

        self.cyclic_count = 0
        self.dt = 0.01
        self.timer = mmtimer(int(self.dt*1000), self.cyclicTransmit) # inveral = 10ms, resoltion = 0
        self.is_running = True
        self.timer.start()

    def scenarioPlay(self):
        self.scenario_play = CanStatus.START

    def scenarioStop(self):
        self.scenario_play = CanStatus.STOP
        
    def cyclicPlay(self):
        self.cyclic_play = CanStatus.START

    def CyclicStop(self):
        self.cyclic_play = CanStatus.STOP
        
    def scenarioMessage(self, ch, cycle_time, msg, msgData):
        self.scenarioQueue.put([ch, cycle_time, msg, msgData])

    def cyclicMessage(self, ch, cycle_time, msg, msgData):
        self.cyclicQueue.put([ch, cycle_time, msg, msgData])

    def eventMessage(self, ch, msg, msgData):
        self.eventQueue.put([ch, msg, msgData])

    def scenarioTransmit(self, scenario_count):
        if self.scenario_play == CanStatus.START:
            self.scenarioMessages = dict()
            
            for _ in range(self.scenarioQueue.qsize()):
                if not self.scenarioQueue.empty():
                    [ch, cycle_time, scenario_msg, scenario_msgData] = self.scenarioQueue.get(False)
                    self.scenarioMessages[scenario_msg.frame_id] = [ch, cycle_time, scenario_msgData]
            
            for scenario_msg.frame_id in self.scenarioMessages:
                scenario_sendMsg = can.Message(arbitration_id = scenario_msg.frame_id, data = self.scenarioMessages[scenario_msg.frame_id][2], is_fd = True, is_extended_id = False)
                
                if (scenario_count % (self.scenarioMessages[scenario_msg.frame_id][1]/10) == 0):
                    if self.scenarioMessages[scenario_msg.frame_id][0] >= 0 and self.scenarioMessages[scenario_msg.frame_id][0] < 4:
                        self.bus[self.scenarioMessages[scenario_msg.frame_id][0]].send(scenario_sendMsg)
        else:
            self.scenarioMessages = dict()
                    
    def cyclicTransmit(self):
        if (self.cyclic_play == CanStatus.START or self.cyclic_play == CanStatus.LIST_CLEAR):
            self.cyclic_count = self.cyclic_count + 1
            
            if (self.cyclic_play == CanStatus.START):
                self.cyclicMessages = dict()
            
            for _ in range(self.cyclicQueue.qsize()):
                [ch, cycle_time, cyclic_msg, cyclic_msgData] = self.cyclicQueue.get(False)
                self.cyclicMessages[cyclic_msg.frame_id] = [ch, cycle_time, cyclic_msgData]
            
            for frame_id in self.cyclicMessages:
                cyclic_sendMsg = can.Message(arbitration_id = frame_id, data = self.cyclicMessages[frame_id][2], is_fd = True, is_extended_id = False)
                
                if (self.cyclic_count % (self.cyclicMessages[frame_id][1]/10) == 0):
                    if self.cyclicMessages[frame_id][0] >= 0 and self.cyclicMessages[frame_id][0] < 4:
                        self.bus[self.cyclicMessages[frame_id][0]].send(cyclic_sendMsg)
                    
            if (self.cyclic_count == 1000):
                self.cyclic_count = 0
                
            self.cyclic_play = CanStatus.LIST_CLEAR
        else:
            self.cyclicMessages = dict()
            self.cyclic_count = 0
        
    def eventTransmit(self):
        if not self.eventQueue.empty():
            for _ in range(self.eventQueue.qsize()):
                [ch, msg, msgData] = self.eventQueue.get(False)
                sendMsg = can.Message(arbitration_id = msg.frame_id, data = msgData, is_fd = True, is_extended_id = False)
                if ch >= 0 and ch < 4:
                    self.bus[ch].send(sendMsg)