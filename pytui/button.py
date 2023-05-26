import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5 import *

class Button(QWidget):
    
    def __init__(self):
        super().__init__()
        self.initUI()
        
    def initUI(self):
        grid = QGridLayout()
        grid.addWidget(self.firstGroup(), 0, 0)
        self.setLayout(grid)
        
    def firstGroup(self):
        groupbox = QGroupBox('버튼')
        
        layout = QFormLayout()
        
        self.btn_on1 = QPushButton('ON/OFF',self)
        self.btn_on1.setCheckable(True)
        self.btn_on1.clicked.connect(self.Onoff)
    
        self.btn_on2 = QPushButton('ON/OFF',self)
        self.btn_on2.setCheckable(True)
        self.btn_on2.clicked.connect(self.Onoff)
        
        self.btn_on3 = QPushButton('ON/OFF',self)
        self.btn_on3.setCheckable(True)
        self.btn_on3.clicked.connect(self.Onoff)
        
        self.btn_on4 = QPushButton('ON/OFF',self)
        self.btn_on4.setCheckable(True)
        self.btn_on4.clicked.connect(self.Onoff)
        
        hbox1 = QHBoxLayout()
        hbox1.addWidget(QLabel('RCCA'))
        hbox1.addWidget(self.btn_on1)
        
        hbox2 = QHBoxLayout()
        hbox2.addWidget(QLabel('SEA'))
        hbox2.addWidget(self.btn_on2)
        
        hbox3 = QHBoxLayout()
        hbox3.addWidget(QLabel('BCA'))
        hbox3.addWidget(self.btn_on3)
        
        hbox4 = QHBoxLayout()
        hbox4.addWidget(QLabel('RESET'))
        hbox4.addWidget(self.btn_on4)

        layout.addRow(hbox1)
        layout.addRow(hbox2)
        layout.addRow(hbox3)
        layout.addRow(hbox4)
        groupbox.setLayout(layout)
        return groupbox
    
    def Onoff(self):
        if self.btn_on1.isChecked():
            self.btn_on1.setText('ON')
            
        else:
            self.btn_on1.setText('ON/OFF')
            
        if self.btn_on2.isChecked():
            self.btn_on2.setText('ON')
            
        else:
            self.btn_on2.setText('ON/OFF')
            
        if self.btn_on3.isChecked():
            self.btn_on3.setText('ON')
            
        else:
            self.btn_on3.setText('ON/OFF')
            
        if self.btn_on4.isChecked():
            self.btn_on4.setText('ON')
            
        else:
            self.btn_on4.setText('ON/OFF')