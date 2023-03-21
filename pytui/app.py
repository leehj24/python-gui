import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5 import *
from pandas import *
import pandas as pd
import matplotlib.pyplot as plt
import pyqtgraph as pg
import logging
from pathlib import Path
from birdeyeview import *
class MyApp(QMainWindow):
    trackList = [Track(50, 50), Track(80,80),Track(110, 110)]
    leftLane=[Lane(-1,5,1,1)]
    rightLane=[Lane(1,5,1,1)]
    
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
        self.setGeometry(300, 50, 500, 800)
        self.show()
        
    def firstGroup(self):
        groupbox = QGroupBox('파일')
        btn_2 = QPushButton('select_csv', self)
        btn_2.clicked.connect(self.file_op)
        
        self.filename = QLineEdit()
        hbox = QHBoxLayout()
        hbox.addWidget(QLabel('File'))
        hbox.addWidget(self.filename)
        hbox.addWidget(btn_2)
    
        groupbox.setLayout(hbox)
        return groupbox
    
    def secondGroup(self):
        groupbox = QGroupBox('버튼')
        
        layout = QFormLayout()
        button = QHBoxLayout()
    
        btn2 = QPushButton('select_csv', self)
        btn2.clicked.connect(self.select_csv)
        
        btn3 = QPushButton('play', self)
        btn3.clicked.connect(self.play)
        
        btn4 = QPushButton('stop', self)
        btn4.clicked.connect(self.stop)
        
        button.addWidget(btn2)
        button.addWidget(btn3)
        button.addWidget(btn4)
        
        self.step = 0
        
        self.slider = QSlider(Qt.Horizontal, self)
        self.slider.valueChanged.connect(self.slider.setValue)
        
        vbox = QVBoxLayout()
        vbox.addWidget(self.slider)
        
        hbox = QHBoxLayout()
        hbox.addWidget(btn2)
        hbox.addWidget(btn3)
        hbox.addWidget(btn4)
        
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
    
    def file_op(self):
        file_name, self.file = QFileDialog.getOpenFileName(self) 
        if file_name:
            path = Path(file_name)
            self.filename.setText(str(path))
            
    def select_csv(self):
        file = QFileDialog.getOpenFileName(self)   
        # if file:
        #     path = Path(file)
        #     self.filename.setText(str(path))
                 
        data = pd.read_csv(file[0])
        plt.plot(data.num, data.a)
        plt.plot(data.num, data.a1)
        plt.plot(data.num, data.b)
        plt.plot(data.num, data.b1)
        # print (data)
        plt.show()
        
    def log(self):
        groupbox = QGroupBox('로그')
        logTextBox = QTextBrowser(self)
        logTextBox.setAcceptRichText(True)
        logTextBox.setOpenExternalLinks(True)

        logging.getLogger().setLevel(logging.DEBUG)
        # logging.debug('debug')
        # logging.info('info')
        
        text = logging.debug,logging.info
        logTextBox.append(str(text))
        
        # log_1 = QScrollArea()
        vbox = QVBoxLayout()
        vbox.addWidget(logTextBox)
        groupbox.setLayout(vbox)
        return groupbox
        
    def timeout_run(self):
        if self.isStart:
            for track in self.trackList:
                track.x = track.x + 3
            self.bev.setTrackList(self.trackList)
            self.bev.setLane(self.leftLane)
            self.bev.setlane(self.rightLane)
             
            if self.step >= 100:
                self.step=0
                # self.timer.stop()
                return
            
            self.step = self.step + 1
            self.slider.setValue(self.step)
        
    def play(self):
        if not self.isStart:
            self.timer = QTimer(self)
            self.timer.start(50)
            self.timer.timeout.connect(self.timeout_run)
            self.isStart = True

    def stop(self):
        self.timer.stop()
        self.isStart = False
     
if __name__ == '__main__':
    app = QApplication(sys.argv)
    myapp = MyApp()
    myapp.show()
    app.exec_()
