import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5 import *
from pandas import *
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
from birdeyeview import *

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
        btn_2 = QPushButton('select_csv', self)
        btn_2.clicked.connect(self.file_op)
        
        layout = QFormLayout()

        self.filename = QLineEdit()
  
        hbox = QHBoxLayout()
        hbox.addWidget(QLabel('File'))
        hbox.addWidget(self.filename)
        hbox.addWidget(btn_2)
        
        layout.addRow(hbox)
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
        
    def timeout_run(self):
        self.bev1 = BirdEyeView1()
        if self.isStart:
            for track in self.trackList:
                track.x = track.x + 1
                
            # self.bev.setTrackList(self.trackList)
            self.bev.setTrackList(self.trackList)
            self.bev1.setlane_left(self.leftLane)
            self.bev1.setlane_right(self.rightLane)
             
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
# http://www.guud.com/shop/goodsView?itemId=54326
#벽시계