#!/usr/bin/env python
import can
from can.message import Message
from threading import*
import queue
import time

class CanTransmit:
    def __init__(self, ch):
        self.bus = can.interface.Bus(bustype = 'vector', channel = ch)
        self.ms = 0.01

        self.periodMessages = dict()
        self.manualMessages = dict()
        
        self.periodQueue = queue.Queue()
        self.manualQueue = queue.Queue()
        
        self.play = False
        self.exit = False

        thread = Thread(target = self.threadTransmit, args = ())
        thread.start()

    def start(self):
        self.play = True

    def stop(self):
        self.play = False
        
    def terminate(self):
        self.exit = True

    def updateMessage(self, msg, msgData, period):
        self.periodQueue.put([msg, msgData])
        self.ms = period/1000
        
    def manualMessage(self, msg, msgData):
        self.manualQueue.put([msg, msgData])

    def threadTransmit(self):
        while(1):
            if self.play:
                if not self.periodQueue.empty():
                    [msg, msgData] = self.periodQueue.get(False)
                    self.periodMessages[msg.frame_id] = [msg, msgData]
                
                for msg.frame_id in self.periodMessages:
                    sendMsg = can.Message(arbitration_id = msg.frame_id, data = msgData, is_fd = True, is_extended_id = False)
                    self.bus.send(sendMsg)
                    
            if self.exit:
                break
   
            time.sleep(self.ms)
            
    def onceTransmit(self):
        if not self.manualQueue.empty(): 
            for _ in range(self.manualQueue.qsize()):
                [msg, msgData] = self.manualQueue.get(False)
                self.manualQueue.put([msg, msgData])
                self.manualMessages[msg.frame_id] = [msg, msgData]
            
        for msg.frame_id in self.manualMessages: 
            sendMsg = can.Message(arbitration_id = msg.frame_id, data = msgData, is_fd = True, is_extended_id = False)
            self.bus.send(sendMsg)

if __name__ == "__main__":
    canTx = CanTransmit(1)