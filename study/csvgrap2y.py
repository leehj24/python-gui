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

class Track:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        
class BirdEyeView(QMainWindow):
    
    trackList = [Track(-5, -5)]

    def __init__(self):
        super().__init__()
        self.x = 0
        self.y = 0
        
        self.label = QLabel()
        self.canvas =QPixmap('car.png')
        self.label.setPixmap(self.canvas)
        widget = QWidget()
        
        # vbox = QVBoxLayout(widget)
        # vbox.addWidget(self.label)
        self.setCentralWidget(widget)
        
    def paintEvent(self, e):
        qp = QPainter(self.label.pixmap())
        self.timer = QTimer(self)
        self.timer.start(300)
        self.timer.timeout.connect(self.update_canvas)
        
        # qp.begin(self)      -painter already active 로그창 
        self.draw_objects(qp)
        # qp.end()
        # self.update()

    def draw_objects(self,qp):
        qp.setPen(QPen(Qt.yellow, 8))
        
        for track in self.trackList:
            qp.drawPoint(track.x, track.y)
            
    def update_canvas(self):
        self.label = QLabel()
        self.canvas =QPixmap('car.png')
        self.label.setPixmap(self.canvas)
        widget = QWidget()
        
        vbox = QVBoxLayout(widget)
        vbox.addWidget(self.label)
        self.setCentralWidget(widget)
            
    def setTrackList(self, trackList):  
        self.trackList = trackList
               
class MyApp(QWidget):
    trackList = [Track(50, 50), Track(80,80),Track(110, 110)]
    
        
    def __init__(self):
        super().__init__()
        self.initUI()  
    
    def initUI(self):
        grid = QGridLayout()
     
        self.bev = BirdEyeView()

        grid.addWidget(self.bev, 1, 0) 
        
        self.lb = QLabel(self)
        
        grid.addWidget(self.firstGroup(), 0, 0)
        grid.addWidget(self.secondGroup(), 2, 0)# 버튼
        # grid.addWidget(self.thirdGroup(), 3, 0)#테이블
        # grid.addWidget(self.lb, 3, 0)
        grid.addWidget(self.log(), 4, 0) #QTextBrowser, QScrollArea
              
        self.setLayout(grid)
        grid = QGridLayout()
        
        self.setWindowTitle('Absolute Positioning')
        self.setGeometry(300, 50, 500, 800)
        self.show()
        
    def firstGroup(self):
        groupbox = QGroupBox('파일')
        btn_2 = QPushButton('select_csv', self)
        btn_2.clicked.connect(self.select_csv)
        
        self.filename = QLineEdit()
        hbox = QHBoxLayout()
        hbox.addWidget(QLabel('File'))
        hbox.addWidget(self.filename)
        hbox.addWidget(btn_2)
    
        groupbox.setLayout(hbox)
        return groupbox
    
    def secondGroup(self):
        groupbox = QGroupBox('버튼')
        
        self.pbar = QProgressBar(self)
        self.pbar.setGeometry(150,650,200,25)
        
        # btn1 = QPushButton('click', self)
        # btn1.clicked.connect(self.buttonClicked)
        
        btn2 = QPushButton('select_csv', self)
        btn2.clicked.connect(self.select_csv)
        # btn2.clicked.connect(self.button_load)
        
        btn3 = QPushButton('play', self)
        btn3.clicked.connect(self.play)
        
        btn4 = QPushButton('stop', self)
        btn4.clicked.connect(self.stop)
        
        self.timer = QBasicTimer()
        self.step = 0
        
        vbox = QVBoxLayout()
        vbox.addWidget(self.pbar)
        
        hbox = QHBoxLayout()
        # hbox.addWidget(btn1)
        hbox.addWidget(btn2)
        hbox.addWidget(btn3)
        hbox.addWidget(btn4)
        groupbox.setLayout(hbox)
        
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
        logging.debug('debug')
        logging.info('info')
        
        # log_1 = QScrollArea()
        vbox = QVBoxLayout()
        vbox.addWidget(logTextBox)
        groupbox.setLayout(vbox)
        return groupbox


    def buttonClicked(self):
        self.lb.setText('self.x,y')
        
        
    def timeout_run(self):
        for track in self.trackList:
            track.x = track.x + 3
            
        self.bev.setTrackList(self.trackList)
        if self.step >= 100:
            self.timer.stop()
            return
        
        self.step = self.step + 1
        self.pbar.setValue(self.step)
        
    def play(self):
        self.timer = QTimer(self)
        self.timer.start(80)
        self.timer.timeout.connect(self.timeout_run)

    def stop(self):
        self.timer.stop()        
     
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyApp()
    ex.show()
    app.exec_()
    # sys.exit(app.exec_())