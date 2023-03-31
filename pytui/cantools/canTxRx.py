#!/usr/bin/env python
import can
import cantools
from can.message import Message
from threading import*
import queue
import time

class CanTransmit:
    def __init__(self, ch):
        self.bus = can.interface.Bus(bustype = 'vector', channel = ch)
        self.ms = 0.01
        # self.begin = 0
        # self.end = 1

        self.periodMessages = dict()
        self.manualMessages = dict()
        # self.rampMessages = dict()
        
        self.periodQueue = queue.Queue()
        self.manualQueue = queue.Queue()
        # self.rampQueue = queue.Queue()
        
        self.play = False

        thread = Thread(target = self.threadTransmit, args = ())
        thread.start()

    def start(self):
        self.play = True

    def stop(self):
        self.play = False

    def updateMessage(self, msg, msgData, period): # Data를 받아서 Queue에 저장
        self.periodQueue.put([msg, msgData])
        self.ms = period/1000
        
    def manualMessage(self, msg, msgData):
        self.manualQueue.put([msg, msgData])
        
    # def rampMessage(self, msg, msgData, a, b):
    #     self.rampQueue.put([msg, msgData])
    #     self.begin = a
    #     self.end = b

    def threadTransmit(self):
        while(1):
            if self.play:
                if not self.periodQueue.empty(): # empty가 아니라면 Queue에서 msg, msgData 반환
                    [msg, msgData] = self.periodQueue.get(False)
                    self.periodMessages[msg.frame_id] = [msg, msgData]
                
                for msg.frame_id in self.periodMessages: # canMessages에 있는 msg, msgData 이용
                    sendMsg = can.Message(arbitration_id = msg.frame_id, data = msgData, is_fd = True, is_extended_id = False)
                    self.bus.send(sendMsg)
   
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
            
    # def rampTransmit(self):
    #     for _ in range(self.end - self.begin):
    #         if not self.rampQueue.empty():
    #             [msg, msgData] = self.rampQueue.get(False)
    #             self.rampQueue.put([msg, msgData])
    #             self.rampMessages[msg.frame_id] = [msg, msgData]
                    
    #         for msg.frame_id in self.rampMessages: 
    #             sendMsg = can.Message(arbitration_id = msg.frame_id, data = msgData, is_fd = True, is_extended_id = False)
    #             print(sendMsg.data)
    #             self.bus.send(sendMsg)
                
    #         time.sleep(self.ms)

if __name__ == "__main__":
    canTx = CanTransmit(1)