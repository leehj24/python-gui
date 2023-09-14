#!/usr/bin/env python
from ctypes import *
from ctypes.wintypes import UINT
from ctypes.wintypes import DWORD

timeproc = WINFUNCTYPE(None, c_uint, c_uint, DWORD, DWORD, DWORD)
timeSetEvent = windll.winmm.timeSetEvent
timeKillEvent = windll.winmm.timeKillEvent


class mmtimer:

    def __init__(self, interval, tickFunc, *args, **kwargs):
        self.interval = UINT(interval)
        self.resolution = UINT(0)
        self.tickFunc = tickFunc
        #self.stopFunc = stopFunc
        self.periodic = True
        self.id = None
        self.running = False
        self.calbckfn = timeproc(self.CallBack)
        #
        self.args = args
        self.kwargs = kwargs

    def Tick(self):

        self.tickFunc(*self.args, **self.kwargs)

        if not self.periodic:
            self.stop()

    def CallBack(self, uID, uMsg, dwUser, dw1, dw2):
        if self.running:
            self.Tick()

    def start(self, instant=False):
        if not self.running:
            self.running = True
            if instant:
                self.Tick()

            self.id = timeSetEvent(self.interval, self.resolution,
                                   self.calbckfn, c_ulong(0),
                                   c_uint(self.periodic))

    def stop(self):
        if self.running:
            timeKillEvent(self.id)
            self.running = False
            #if self.stopFunc:
                #self.stopFunc()


if __name__ == '__main__':

    import time

    def tick():
        print("{0:.2f}".format(time.perf_counter() * 1000))

    t1 = mmtimer(10, tick)
    time.perf_counter()
    t1.start(True)
    time.sleep(2)
    t1.stop()