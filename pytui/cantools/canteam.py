#!/usr/bin/env python
import can
import cantools
from can.message import Message
from threading import*
import queue
import time

class CanTransmit:
    def __init__(self, ch): # msg, msgData
        self.bus = can.interface.Bus(bustype = 'vector', channel = ch)

        self.canMessages = dict() # List가 아닌 Dict로 접근
        self.dataQueue = queue.Queue()

        thread1 = Thread(target = self.threadTransmit, args = ())
        thread2 = Thread(target = self.updateMessage, args = ())

        thread1.start()
        thread2.start()

    def registerMessage(self, msg, msgData):
        self.canMessages[msg.frame_id] = [msg, msgData]
        
    def updateMessage(self, msg, msgData): # Data를 받아서 Queue에 저장
        self.dataQueue.put([msg, msgData])

    def threadTransmit(self):
        ms = float(input())
        
        while(1):
            if not self.dataQueue.empty(): # empty가 아니라면 Queue에서 msg, msgData 반환
                [msg, msgData] = self.dataQueue.get(False)
                self.canMessages[msg.frame_id] = [msg, msgData]
            
            for msg.frame_id in self.canMessages: # canMessages에 있는 msg, msgData 이용
                sendMsg = can.Message(arbitration_id = msg.frame_id, data = msgData, is_fd = True, is_extended_id = False)
                self.bus.send(sendMsg)
            
            time.sleep(ms)

if __name__ == "__main__":
    canTx = CanTransmit(1)