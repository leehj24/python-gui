#!/usr/bin/env python
import os
import sys
import subprocess
import time
import threading
from win32com.client import *
from win32com.client.connect import *

class CANoe:
    def __init__(self):
        self.application = None
        self.application = win32com.client.DispatchEx("CANoe.Application")
        self.ver = self.application.Version
        
        print('Loaded CANoe version ',
            self.ver.major, '.',
            self.ver.minor, '.',
            self.ver.Build, '...')
        
    def open_simulation(self, cfgname):
        if (self.application != None):
            if os.path.isfile(cfgname) and (os.path.splitext(cfgname)[1] == ".cfg"):
                self.application.Open(cfgname)
                print(self.application.Environment.GetVariable)
            else:
                raise RuntimeError("Can't find CANoe cfg file")
        else:
            raise RuntimeError("CANoe Application is missing, unable to open simulation")

    def close_simulation(self):
        if (self.application != None):
            self.stop_Measurement()
            self.application.Quit()

        # output = subprocess.check_output('tasklist', shell=True)
        # if "CANoe64.exe" in str(output):
        #     os.system("taskkill /im CANoe64.exe /f 2>nul >nul")
        #     print("CANoe killed")

        self.application = None
        
    def start_Measurement(self):
            retry = 0
            retry_counter = 5
            
            while not self.application.Measurement.Running and (retry < retry_counter):
                self.application.Measurement.Start()
                time.sleep(1)
                retry += 1
            if (retry == retry_counter):
                raise RuntimeWarning("CANoe start measuremet failed, Please Check Connection!")
        
    def stop_Measurement(self):
        if self.application.Measurement.Running:
            self.application.Measurement.Stop()
        else:
            pass
        
    ############################################################################################
    
    def get_EnvVar(self, var):

        if (self.application != None):
            result = self.application.Environment.GetVariable(var)
            return result.Value
        else:
            raise RuntimeError("CANoe is not open,unable to GetVariable")

    def set_EnvVar(self, var, value):
        result = None

        if (self.application != None):
            # set the environment varible
            result = self.application.Environment.GetVariable(var)
            result.Value = value

            checker = self.get_EnvVar(var)
            # check the environment varible is set properly?
            while (checker != value):
                checker = self.get_EnvVar(var)
        else:
            raise RuntimeError("CANoe is not open,unable to SetVariable")

    def get_SigVal(self, channel_num, msg_name, sig_name, bus_type="CAN"):
        # """
        # @summary Get the value of a raw CAN signal on the CAN simulation bus
        # @param channel_num - Integer value to indicate from which channel we will read the signal, usually start from 1,
                             # Check with CANoe can channel setup.
        # @param msg_name - String value that indicate the message name to which the signal belong. Check DBC setup.
        # @param sig_name - String value of the signal to be read
        # @param bus_type - String value of the bus type - e.g. "CAN", "LIN" and etc.
        # @return The CAN signal value in floating point value.
                # Even if the signal is of integer type, we will still return by
                # floating point value.
        # @exception None
        # """
        if (self.application != None):
            result = self.application.GetBus(bus_type).GetSignal(channel_num, msg_name, sig_name)
            return result.Value
        else:
            raise RuntimeError("CANoe is not open,unable to GetVariable")

    def get_SysVar(self, ns_name, sysvar_name):

        if (self.application != None):
            systemCAN = self.application.System.Namespaces
            sys_namespace = systemCAN(ns_name)
            sys_value = sys_namespace.Variables(sysvar_name)
            return sys_value.Value
        else:
            raise RuntimeError("CANoe is not open,unable to GetVariable")

    def set_SysVar(self, ns_name, sysvar_name, var):

        if (self.application != None):
            systemCAN = self.application.System.Namespaces
            sys_namespace = systemCAN(ns_name)
            sys_value = sys_namespace.Variables(sysvar_name)
            sys_value.Value = var
            # print(sys_value)
            # result = sys_value(sys_name)
            #
            # result = var
        else:
            raise RuntimeError("CANoe is not open,unable to GetVariable")

    def get_all_SysVar(self, ns_name):

        if (self.application != None):
            sysvars=[]
            systemCAN = self.application.System.Namespaces
            sys_namespace = systemCAN(ns_name)
            sys_value = sys_namespace.Variables
            for sys in sys_value:
                sysvars.append(sys.Name)
                sysvars.append(sys.Value)
            return sysvars
        else:
            raise RuntimeError("CANoe is not open,unable to GetVariable")
        
    ############################################################################################
    
if __name__ == '__main__':
    os.chdir("C:\Program Files\Vector CANoe 12.0\Exec64")

    app = CANoe()
    app.open_simulation("D:\CAN_PYTHON\Test_for_CAN_Python.cfg") # measurement보다 먼저 실행해야함
    # app.set_EnvVar(1,1)
    time.sleep(1)
    app.start_Measurement()
    # time.sleep(5)
    # app.close_simulation()