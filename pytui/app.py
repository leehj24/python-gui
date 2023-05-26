import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5 import *
from pandas import *
from pathlib import Path
from birdeyeview import *
from select_file import *
import pandas as pd
import matplotlib.pyplot as plt
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
      
        self.scroll = QScrollArea()
        self.scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.scroll.setWidgetResizable(True)
        self.scroll.setWidget(widget)
        self.setCentralWidget(self.scroll)
        self.setWindowTitle('Absolute Positioning')
        self.setGeometry(300, 50, 1000, 950)
        self.show()
        
    def firstGroup(self): 
        groupbox = QGroupBox('파일')
        file = Openfile()
        hbox = QHBoxLayout()
        hbox.addWidget(file)
        groupbox.setLayout(hbox)
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
        
if __name__ == '__main__':
    app = QApplication(sys.argv)
    myapp = MyApp()
    myapp.show()
    app.exec_()
