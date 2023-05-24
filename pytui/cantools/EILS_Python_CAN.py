#!/usr/bin/env python
import can
from can.message import Message
from threading import *
import queue
import time
import cantools

class CanTransmit:
    def __init__(self, ch):
        self.bus = can.interface.Bus(bustype = 'vector', channel = ch)

        self.scenarioMessages = dict()
        self.cyclicMessages = dict()
        
        self.scenarioQueue = queue.Queue()
        self.cyclicQueue = queue.Queue()
        self.eventQueue = queue.Queue()
        
        self.scenario_play = False
        self.cyclic_play = False
        self.exit_thread = False

        thread = Thread(target = self.Transmit, args = ())
        thread.start()

    def scenarioPlay(self):
        self.scenario_play = True

    def scenarioStop(self):
        self.scenario_play = False
        
    def cyclicPlay(self):
        self.cyclic_play = True

    def CyclicStop(self):
        self.cyclic_play = False
        
    def exitThread(self):
        self.exit_thread = True
        
    def scenarioMessage(self, msg, msgData):
        self.scenarioQueue.put([msg, msgData])

    def cyclicMessage(self, msg, msgData):
        self.cyclicQueue.put([msg, msgData])
        
    def eventMessage(self, msg, msgData):
        self.eventQueue.put([msg, msgData])

    def Transmit(self):
        scenario_count = 0
        cyclic_count = 0
        db = cantools.db.load_file('D:\PythonEILS\Data\HKMC\MX5\ECANFD_MX5_PROTO.0.dbc')
        
        while(1):
            time.sleep(0.01)
            
            if self.scenario_play:
                # print("scenario_play")
                scenario_count = scenario_count + 1
                
                for _ in range(self.scenarioQueue.qsize()):
                    if not self.scenarioQueue.empty():
                        [scenario_msg, scenario_msgData] = self.scenarioQueue.get(False)
                        self.scenarioMessages[scenario_msg.frame_id] = [scenario_msg, scenario_msgData]
                
                for scenario_msg.frame_id in self.scenarioMessages:
                    scenario_sendMsg = can.Message(arbitration_id = scenario_msg.frame_id, data = self.scenarioMessages[scenario_msg.frame_id][1], is_fd = True, is_extended_id = False)
                    scenarioMsg_by_id = db.get_message_by_frame_id(scenario_msg.frame_id)
                    
                    if (scenario_count % (scenarioMsg_by_id.cycle_time/10) == 0):
                        self.bus.send(scenario_sendMsg)
                        
                if (scenario_count==100):
                    scenario_count = 0
            else:
                scenario_count = 0
                    
            if self.cyclic_play:
                # print("cyclic_play")
                cyclic_count = cyclic_count + 1
                
                for _ in range(self.cyclicQueue.qsize()):
                    if not self.cyclicQueue.empty():
                        [cyclic_msg, cyclic_msgData] = self.cyclicQueue.get(False)
                        self.cyclicMessages[cyclic_msg.frame_id] = [cyclic_msg, cyclic_msgData]
                
                for cyclic_msg.frame_id in self.cyclicMessages:
                    cyclic_sendMsg = can.Message(arbitration_id = cyclic_msg.frame_id, data = self.cyclicMessages[cyclic_msg.frame_id][1], is_fd = True, is_extended_id = False)
                    cyclicMsg_by_id = db.get_message_by_frame_id(cyclic_msg.frame_id)
                    
                    if (cyclic_count % (cyclicMsg_by_id.cycle_time/10) == 0):
                        self.bus.send(cyclic_sendMsg)
                        
                if (cyclic_count==100):
                    cyclic_count = 0
            else:
                cyclic_count = 0
                    
            if self.exit_thread:
                break
            
    def eventTransmit(self):
        if not self.eventQueue.empty():
            for _ in range(self.eventQueue.qsize()):
                [msg, msgData] = self.eventQueue.get(False)
                sendMsg = can.Message(arbitration_id = msg.frame_id, data = msgData, is_fd = True, is_extended_id = False)
                self.bus.send(sendMsg)

if __name__ == "__main__":
    canTx = CanTransmit(1)