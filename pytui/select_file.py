import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5 import *
import json
class Openfile(QWidget):
    
    def __init__(self):
        super().__init__()
        self.initUI()
        
    def initUI(self):
        self.OEM=QComboBox()
        file_path = "./config/oem.json"
        with open(file_path) as file:
            data = json.load(file)
            self.json_test = data['OEM']
        
        for k in self.json_test:
            self.O_Name= k['name']
            self.OEM.addItem(self.O_Name)
        self.OEM.activated[str].connect(self.fileopenActivated)
        
        self.vehicle1=QComboBox()
        self.scenario=QComboBox()
        
        Hbox1 = QHBoxLayout()
        Hbox1.addWidget(QLabel('OEM'))
        Hbox1.addWidget(self.OEM)
        
        Hbox1.addWidget(QLabel('차량'))
        Hbox1.addWidget(self.vehicle1)
        self.vehicle1.activated[str].connect(self.fileopenActivated1)
        
        Hbox1.addWidget(QLabel('시나리오'))
        Hbox1.addWidget(self.scenario)
        self.scenario.setFixedSize(300,25)
        self.setLayout(Hbox1)
        
    def fileopenActivated(self,text):
        if text == 'HKMC':
            self.vehicle1.clear()
            self.scenario.clear()
            for i in range(0,2):
                V_name = self.json_test[0]['vehicles'][i]['name']
                self.vehicle1.addItem(V_name)
        elif text == 'SYMC':
            self.vehicle1.clear()
            self.scenario.clear()
        #     for i in range(0,2):
        #         V_name = self.json_test[1]['vehicles'][i]['name']
        #         self.vehicle1.addItem(V_name)
        elif text == 'LUCID':
            self.vehicle1.clear()
            self.scenario.clear()
        #     for i in range(0,2):
        #         V_name = self.json_test[2]['vehicles'][i]['name']
        #         self.vehicle1.addItem(V_name)
        else:
            self.vehicle1.clear()
            self.scenario.clear()
        #     for i in range(0,2):
        #         V_name = self.json_test[3]['vehicles'][i]['name']
        #         self.vehicle1.addItem(V_name)
                
    def fileopenActivated1(self,text):
        if text == 'RG3':
            self.scenario.clear()
            self.scenario.addItem(self.json_test[0]['vehicles'][0]['can1'])
            self.scenario.addItem(self.json_test[0]['vehicles'][0]['can2'])
          
        elif text == 'RS4':
            self.scenario.clear()
            self.scenario.addItem(self.json_test[0]['vehicles'][1]['can1'])
            self.scenario.addItem(self.json_test[0]['vehicles'][1]['can2'])
        
        # elif text == 'name1':
        #     self.scenario.clear()
        #     self.scenario.addItem(self.json_test[1]['vehicles'][0]['can1'])
        #     self.scenario.addItem(self.json_test[1]['vehicles'][0]['can2'])
            # rodntruzzz
        # elif text == 'name2':
        #     self.scenario.clear()
        #     self.scenario.addItem(self.json_test[1]['vehicles'][1]['can1'])
        #     self.scenario.addItem(self.json_test[1]['vehicles'][1]['can2'])