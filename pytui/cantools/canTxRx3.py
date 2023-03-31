#!/usr/bin/env python
import can
from can.message import Message
from threading import*
import queue
import time
import threading

condition_obj = threading.Condition()

class CanTransmit:
    def __init__(self, ch, condition_obj):
        self.bus = can.interface.Bus(bustype = 'vector', channel = ch)
        self.ms = 0.01

        self.periodMessages = dict()
        self.manualMessages = dict()
        
        self.periodQueue = queue.Queue()
        self.manualQueue = queue.Queue()
        
        self.play = True
        self.exit = False

        thread = Thread(target = self.threadTransmit, args = (condition_obj,))
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

    def threadTransmit(self, condition_obj):
        while(1):
            condition_obj.acquire()
            if self.play:
                condition_obj.notify_all()
                if not self.periodQueue.empty():
                    [msg, msgData] = self.periodQueue.get(False)
                    self.periodMessages[msg.frame_id] = [msg, msgData]
                
                for msg.frame_id in self.periodMessages:
                    sendMsg = can.Message(arbitration_id = msg.frame_id, data = msgData, is_fd = True, is_extended_id = False)
                    self.bus.send(sendMsg)
            else:
                condition_obj.wait(self.ms)
                    
            if self.exit:
                break
   
            condition_obj.wait(self.ms)
            condition_obj.release()
            
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
    canTx = CanTransmit(1,condition_obj)