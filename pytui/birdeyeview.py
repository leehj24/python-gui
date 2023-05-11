from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5 import *
from birdeyeview1 import *
from birdeyeview2 import *
import numpy as np
import os
class Track:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class BirdEyeView(QWidget):
    
    trackList = [Track(-400, 0)]
    scale_factor = 50 #그리드 사이즈 증가
    target_factor = 1 # 타켓차 그리즈 사이즈 변경
    
    def __init__(self):
        super().__init__()
       
        self.label = QLabel()
        self.canvas = QPixmap(self.width(),self.width())
        self.canvas.fill(Qt.black)
        self.label.setPixmap(self.canvas)

        self.car = QPixmap('car.png')
        self.FLbox = QTextBrowser(self)
        self.FRbox = QTextBrowser(self)
        self.RLbox = QTextBrowser(self)
        self.RRbox = QTextBrowser(self)
        
        self.OEM=QComboBox()
        file= os.listdir(os.getcwd())
        for i in range(0, 10): 
            self.OEM.addItem(file[i])
            
        self.OEM.activated[str].connect(self.fileopenActivated)
        
        self.vehicle1=QComboBox()
        self.scenario=QComboBox()
        
        Hbox1 = QHBoxLayout()
        Hbox1.addWidget(QLabel('OEM'))
        Hbox1.addWidget(self.OEM)
        
        Hbox2 = QHBoxLayout()
        Hbox2.addWidget(QLabel('차량'))
        Hbox2.addWidget(self.vehicle1)
        self.vehicle1.activated[str].connect(self.fileopenActivated1)
        
        Hbox3 = QHBoxLayout()
        Hbox3.addWidget(QLabel('시나리오'))
        Hbox3.addWidget(self.scenario)
        
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
        # self.btn_on4.setCheckable(True)
        self.btn_on4.clicked.connect(self.Onoff)
        
        self.Layout = QVBoxLayout(self)
        
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

        self.qvbox= QVBoxLayout()
        self.qvbox.addLayout(Hbox1)
        self.qvbox.addLayout(Hbox2)
        self.qvbox.addLayout(Hbox3)
        self.qvbox.addLayout(hbox1)
        self.qvbox.addLayout(hbox2)
        self.qvbox.addLayout(hbox3)
        self.qvbox.addLayout(hbox4)

        self.cido=QHBoxLayout()
        self.cido.addWidget(self.label)
        self.cido.addLayout(self.qvbox)
        
        self.fl_fr = QHBoxLayout()
        self.fl_fr.addWidget(QLabel('FL'))
        self.fl_fr.addWidget(self.FLbox)
        self.fl_fr.addWidget(QLabel('FR'))
        self.fl_fr.addWidget(self.FRbox)
        
        self.rl_rr = QHBoxLayout(self)
        self.rl_rr.addWidget(QLabel('RL'))
        self.rl_rr.addWidget(self.RLbox)
        self.rl_rr.addWidget(QLabel('RR'))
        self.rl_rr.addWidget(self.RRbox)
        
        self.Layout.addLayout(self.cido)
        self.Layout.addLayout(self.fl_fr)
        self.Layout.addLayout(self.rl_rr)
        
        self.setLayout(self.Layout)

        self.center_x = self.canvas.width()/2
        self.center_y = self.canvas.height()/2
        
        self.canvas_x = self.canvas.width()+20
        self.canvas_y = self.canvas.height()+20
        
        self.canvas_x1 = self.canvas.width()-20
        self.canvas_y1 = self.canvas.height()-20
        
        self.timer = QTimer(self)
        self.timer.start(30)
        self.timer.timeout.connect(self.onTimer)
        
    def onTimer(self):
        self.update()
    
    def paintEvent(self, e):
        qp = QPainter(self.label.pixmap())
        qp.fillRect(self.canvas.rect(),Qt.black)

        self.draw_grid(qp) # 그리드 좌표선
        
        self.draw_objects(qp) # object 
        
        qp.end()

    def M2P(self, x_m, y_m):
        point = QPoint()
        point.setX(int(self.center_x + y_m*self.scale_factor))
        point.setY(int(self.center_y - x_m*self.scale_factor))
        return point
    
    def Target(self, x_m, y_m):
        point = QPoint()
        point.setX(int(self.center_x + y_m*self.target_factor))
        point.setY(int(self.center_y - x_m*self.target_factor))
        return point
    
    def draw_grid(self, qp):
    
        qp.drawPixmap(self.M2P(100, -100), self.car)
        
    def draw_objects(self, qp): #타겟
        qp.setPen(QPen(Qt.red, 8))
        
        for self.track in self.trackList:
            qp.drawPoint(self.Target(self.track.x, self.track.y))

    def draw_lane(self, qp,laneVal): #차선
        resolution = 0.5
        qp.setPen(QPen(QColor('#594605'), 1))
        for lane in laneVal:
            for x1 in list(np.arange(-100, 100, resolution)):
                x2 = x1 + resolution
                y1 = lane.a*x1**3 + lane.b*x1**2 + lane.c*x1 + lane.d
                y2 = lane.a*x2**3 + lane.b*x2**2 + lane.c*x2 + lane.d
                qp.drawLine(self.M2P(x1, y1), self.M2P(x2, y2))
            
    def setTrackList(self, trackList):
        self.trackList = trackList
        self.FLbox.append('x값: '+str(self.track.x-5)+
                          '   '+' y값: '+str(self.track.y-5))
        self.FRbox.append('x값: '+str(self.track.x+5)+
                          '   '+' y값: '+str(self.track.y+5))
        self.RLbox.append('x값: '+str(self.track.x-5)+
                          '   '+' y값: '+str(self.track.y-5))
        self.RRbox.append('x값: '+str(self.track.x-5)+
                          '   '+' y값: '+str(self.track.y+5))
        
    def fileopenActivated(self,text):
      
        if text == 'OEM1':
            self.vehicle1.clear()
            root_dir = "./OEM1/"
            for (root, dirs, files) in os.walk(root_dir):
                if len(dirs) > 0:
                    for i in range(0,2):
                        self.vehicle1.addItem(dirs[i])
                      
        elif text == 'OEM2':
            self.vehicle1.clear()
            root_dir = "./OEM2/"
            self.vehicle1.clear()
            for (root, dirs, files) in os.walk(root_dir):
                if len(dirs) > 0:
                    for i in range(0,2):
                        self.vehicle1.addItem(dirs[i])
           
        else:
            self.vehicle1.clear()
            self.scenario.clear()
            
    def fileopenActivated1(self,text):
        if text == 'verticle1':
            self.scenario.clear()
            root_dir = "./OEM1/verticle1/"
            for (root, dirs, files) in os.walk(root_dir):
                if len(files) > 0:
                    for i in range(0,2):
                        self.scenario.addItem(files[i])
                      
        elif text == 'verticle2':
            self.scenario.clear()
            root_dir = "./OEM1/verticle2/"
            for (root, dirs, files) in os.walk(root_dir):
                if len(files) > 0:
                    for i in range(0,2):
                        self.scenario.addItem(files[i])
        
        elif text == 'verticle1.1':
            self.scenario.clear()
            root_dir = "./OEM2/verticle1.1/"
            for (root, dirs, files) in os.walk(root_dir):
                if len(files) > 0:
                    for i in range(0,2):
                        self.scenario.addItem(files[i])
                        
                      
        elif text == 'verticle2.1':
            self.scenario.clear()
            root_dir = "./OEM2/verticle2.1/"
            for (root, dirs, files) in os.walk(root_dir):
                if len(files) > 0:
                    for i in range(0,2):
                        self.scenario.addItem(files[i])
        else:
            self.scenario.clear()
            
    def Onoff(self):
        if self.btn_on1.isChecked():
            self.btn_on1.setText('ON')
            
        else:
            self.btn_on1.setText('ON/OFF')
            
        if self.btn_on2.isChecked():
            self.btn_on2.setText('ON')
            self.bev1 = BirdEyeView1()
            self.cido.addWidget(self.bev1)
            self.cido.removeWidget(self.bev1)
            # self.cido.removeWidget(self.label)
            
        else:
            self.btn_on2.setText('ON/OFF')
            # self.cido.removeWidget(self.bev1)
            
        if self.btn_on3.isChecked():
            self.btn_on3.setText('ON')
            self.bev2 = BirdEyeView2()
            self.cido.addWidget(self.bev2)
            self.cido.removeWidget(self.bev2)
            # self.cido.removeWidget(self.label)
           
        else:
            self.btn_on3.setText('ON/OFF')
            # self.cido.removeWidget(self.bev2)
            
        if self.btn_on4.isChecked():
            self.btn_on4.setText('ON')
            
        else:
            self.btn_on4.setText('ON/OFF')