import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5 import *
from pandas import *
import pandas as pd
import matplotlib.pyplot as plt
import logging
from pathlib import Path
from birdeyeview import *
import os
class MyApp(QMainWindow):
    trackList = [Track(-300, -30)]
    leftLane = [Lane(0, 0, 0, -0.5)]
    rightLane = [Lane(0, 0, 0, 0.5)]
    
    def __init__(self):
        super().__init__()
        self.initUI()

        self.isStart = False  
    
    def initUI(self):

        widget = QWidget()
        grid = QGridLayout(widget)
        
        grid.addWidget(self.firstGroup(), 0, 0)
        grid.addWidget(self.createBevGroup(), 1, 0) 
        grid.addWidget(self.secondGroup(), 2, 0)# 버튼
        grid.addWidget(self.log(), 3, 0) #QTextBrowser, QScrollArea
        
        self.scroll = QScrollArea()
        self.scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.scroll.setWidgetResizable(True)
        self.scroll.setWidget(widget)
        
        self.setCentralWidget(self.scroll)
        self.setWindowTitle('Absolute Positioning')
        self.setGeometry(300, 50, 750, 950)
        self.show()
        
    def firstGroup(self): 
        groupbox = QGroupBox('파일')
        btn_2 = QPushButton('select_csv', self)
        btn_2.clicked.connect(self.file_op)
        
        layout = QFormLayout()

        self.filename = QLineEdit()
        self.vehicle=QLineEdit()
        self.vehicle1=QComboBox()
        self.vehicle1.addItem('Json file')
        self.dbdata=QLineEdit() 
        self.dbdata1=QComboBox()
        self.dbdata1.addItem('CSV file')
        self.dbdata1.addItem('Exvel file')
        
        hbox = QHBoxLayout()
        hbox.addWidget(QLabel('File'))
        hbox.addWidget(self.filename)
        hbox.addWidget(btn_2)

        Hbox = QHBoxLayout()
        Hbox.addWidget(QLabel('차량'))
        Hbox.addWidget(self.vehicle)
        Hbox.addWidget(self.vehicle1)
        
        hBox = QHBoxLayout()
        hBox.addWidget(QLabel('data'))
        hBox.addWidget(self.dbdata)
        hBox.addWidget(self.dbdata1)
        
        self.btn_on1 = QPushButton('ON/OFF',self)
        self.btn_on1.setCheckable(True)
        self.btn_on1.clicked.connect(self.Onoff)
    
        self.btn_on2 = QPushButton('ON/OFF',self)
        self.btn_on2.setAutoExclusive(False)
        self.btn_on2.setCheckable(True)
        self.btn_on2.clicked.connect(self.Onoff)
        
        self.btn_on3 = QPushButton('ON/OFF',self)
        self.btn_on3.setAutoExclusive(False)
        self.btn_on3.setCheckable(True)
        self.btn_on3.clicked.connect(self.Onoff)
        
        self.btn_on4 = QPushButton('ON/OFF',self)
        self.btn_on4.setAutoExclusive(False)
        self.btn_on4.setCheckable(True)
        self.btn_on4.clicked.connect(self.Onoff)
        
        hbox1 = QHBoxLayout()
        hbox1.addWidget(QLabel('RRSA'))
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
        
        layout.addRow(hbox)
        layout.addRow(Hbox)
        layout.addRow(hBox)
        layout.addRow(hbox1)
        layout.addRow(hbox2)
        layout.addRow(hbox3)
        layout.addRow(hbox4)
        
        groupbox.setLayout(layout)
        return groupbox
    
    def secondGroup(self):
        groupbox = QGroupBox('버튼')
        
        layout = QFormLayout()
        button = QHBoxLayout()

        btn = QPushButton('play', self)
        btn.clicked.connect(self.play)
        
        btn2 = QPushButton('stop', self)
        btn2.clicked.connect(self.stop)
        
        button.addWidget(btn)
        button.addWidget(btn2)
        
        self.step = 0
        
        self.slider = QSlider(Qt.Horizontal, self)
        self.slider.valueChanged.connect(self.slider.setValue)
        
        vbox = QVBoxLayout()
        vbox.addWidget(self.slider)
        
        hbox = QHBoxLayout()
        hbox.addWidget(btn)
        hbox.addWidget(btn2)
        
        layout.addRow(vbox)
        layout.addRow(button)

        groupbox.setLayout(layout)
        
        return groupbox
    
    def createBevGroup(self):
        self.bev = BirdEyeView()

        vbox = QVBoxLayout()
        vbox.addWidget(self.bev)
        groupbox = QGroupBox('BirdEyeView')
        groupbox.setLayout(vbox)

        return groupbox
    
    def file_op(self): # 파일선택
        file_name, self.file = QFileDialog.getOpenFileName(self) 
        if file_name:
            path = Path(file_name)
            self.filename.setText(str(path)) #파일 경로
            
        # txt = path.read_text() #선택한 파일 읽기
        # f=open('data.csv','w',encoding='utf-8',newline="")
        # f.write(txt) #파일 저장
        # f.close()
        
        # data = pd.read_csv("data.csv") #저장한 파일 pd로 읽기
        # plt.plot(data.num, data.a)
        # plt.plot(data.num, data.a1)
        # plt.plot(data.num, data.b)
        # plt.plot(data.num, data.b1)
        # plt.show()
        
    def log(self):
        groupbox = QGroupBox('로그')
        logTextBox = QTextBrowser(self)
        logTextBox.setAcceptRichText(True)
        logTextBox.setOpenExternalLinks(True)

        logging.getLogger().setLevel(logging.DEBUG)
        
        text = logging.debug,logging.info
        logTextBox.append(str(self.trackList))
        
        vbox = QVBoxLayout()
        vbox.addWidget(logTextBox)
        groupbox.setLayout(vbox)
        return groupbox
        
    def timeout_run(self):
        if self.isStart:
            for track in self.trackList:
                track.x = track.x + 1
                
            self.bev.setTrackList(self.trackList)
            self.bev.setlane_left(self.leftLane)
            self.bev.setlane_right(self.rightLane)
             
            if self.step >= 100:
                self.step=0
                return
            
            self.step = self.step + 0.5
            self.slider.setValue(int(self.step))
        
    def play(self):
        if not self.isStart:
            self.timer = QTimer(self)
            self.timer.start(50)
            self.timer.timeout.connect(self.timeout_run)
            self.isStart = True

    def stop(self):
        self.timer.stop()
        self.isStart = False
        
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
            
            
    
    # def OnOFF(self):
    #     self.btn_off1.setText('On')
     
if __name__ == '__main__':
    app = QApplication(sys.argv)
    myapp = MyApp()
    myapp.show()
    app.exec_()
