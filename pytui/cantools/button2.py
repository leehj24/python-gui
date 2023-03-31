#!/usr/bin/env python
# from canTxRx2 import *
# from main_can2 import *
import cantools
from can.message import Message
from threading import*
from tkinter import *
import numpy as np
import pandas as pd

# pause = 1

# class ButtonGUI:
#     def __init__(self):

#         threadGUI = Thread(target = self.GUI, args = ())
#         threadGUI.start()

#     def GUI(self):
#         global pause
        
#         tk = Tk()
#         tk.title('CAN Test')
#         tk.minsize(width = 200, height = 200)
#         tk.maxsize(width = 200, height = 200)
#         pause = 0
        
#         def can_start():
#             global pause
#             pause = 1
#             print(pause)
            
#         def can_stop():
#             global pause
#             pause = 0
#             print(pause)

#         btn_can1 = Button(tk, text = 'can_start', command = can_start)
#         btn_can2 = Button(tk, text = 'can_stop', command = can_stop)
        
#         btn_can1.place(x = 73, y = 45)
#         btn_can2.place(x = 73, y = 110)
        
#         tk.mainloop()

# if __name__ == "__main__":
#     button = ButtonGUI()

def GUI():
    tk = Tk()
    tk.title('CAN Test')
    tk.minsize(width = 200, height = 200)
    tk.maxsize(width = 200, height = 200)

    pause = 1
    print(pause)
            
    def can_start():
        pause = 1
        print(pause)
                
    def can_stop():
        pause = 0
        print(pause)

    btn_can1 = Button(tk, text = 'can_start', command = can_start)
    btn_can2 = Button(tk, text = 'can_stop', command = can_stop)
            
    btn_can1.place(x = 73, y = 45)
    btn_can2.place(x = 73, y = 110)
            
    tk.mainloop()
    
thread1 = Thread(target = GUI, args = ())