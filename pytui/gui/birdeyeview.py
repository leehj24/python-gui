from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5 import *
from gui.button import *
import numpy as np

class Track:
    def __init__(self, x, y):
        self.x = x
        self.y = y
class Lane:
    def __init__(self, a, b, c, d):
        self.a = a
        self.b = b
        self.c = c
        self.d = d
class BirdEyeView(QWidget):
    
    trackList = [Track(-400, 0)]
    leftLane = [Lane(0, 0, 0, -0.5)] #0.0001, 0.01, -0.174, -1.5
    rightLane = [Lane(0, 0, 0, 0.5)] #0.0001, 0.01, -0.174, 1.5
    scale_factor = 50 #그리드 사이즈 증가
    target_factor = 1 # 타켓차 그리즈 사이즈 변경
    
    def __init__(self):
        super().__init__()
        
        self.label = QLabel()
        self.canvas = QPixmap(self.width(),self.width())
        self.canvas.fill(Qt.black)
        self.label.setPixmap(self.canvas)
        
        self.car = QPixmap('gui/car.png')
        self.FLbox = QTextBrowser(self)
        self.FRbox = QTextBrowser(self)
        self.RLbox = QTextBrowser(self)
        self.RRbox = QTextBrowser(self)
        
        self.opfile = Button()
        
        self.hbox = QHBoxLayout()
        
        self.fl_fr = QHBoxLayout()
        self.fl_fr.addWidget(QLabel('FL'))
        self.fl_fr.addWidget(self.FLbox)
        self.fl_fr.addWidget(QLabel('FR'))
        self.fl_fr.addWidget(self.FRbox)
        
        self.rl_rr = QHBoxLayout()
        self.rl_rr.addWidget(QLabel('RL'))
        self.rl_rr.addWidget(self.RLbox)
        self.rl_rr.addWidget(QLabel('RR'))
        self.rl_rr.addWidget(self.RRbox)
        
        self.hbox.addWidget(self.opfile)
        self.hbox.addWidget(self.label)

        self.Layout=QVBoxLayout()
        self.Layout.addLayout(self.hbox)
        self.Layout.addLayout(self.fl_fr)
        self.Layout.addLayout(self.rl_rr)
        
        self.setLayout(self.Layout)
        
        self.center_x = self.canvas.width()/2
        self.center_y = self.canvas.height()/2
        
        self.timer = QTimer(self)
        self.timer.start(30)
        self.timer.timeout.connect(self.onTimer)
        print(self.update())
        
    def onTimer(self):
        self.update()
    
    def paintEvent(self, e):
        qp = QPainter(self.label.pixmap())
        qp.fillRect(self.canvas.rect(),Qt.black)

        self.draw_grid(qp) # 그리드 좌표선
        self.draw_objects(qp) # object 
        self.draw_lane(qp, self.leftLane)
        self.draw_lane(qp, self.rightLane)
        self.target_lane(qp)
        
        qp.end()

    def M2P(self, x_m, y_m):
        point = QPoint()
        point.setX(int(self.center_x + y_m*self.scale_factor))
        point.setY(int(self.center_y - x_m*self.scale_factor))
        return point

    def draw_grid(self, qp):

        # qp.setPen(QPen(QColor('#4A4A4A'), 1)) # 좌표선 
        # for x_1 in range(-100,100):
        #     for y_1 in range(-100,100):
        #         qp.drawLine(self.M2P(x_1, y_1), self.M2P(x_1, -y_1)) # y선
        #         qp.drawLine(self.M2P(-x_1, y_1), self.M2P(x_1, y_1)) # x선
                
        qp.setPen(QPen(Qt.gray, 1)) 
        # qp.drawLine(self.M2P(0, -100), self.M2P(0, 100)) #중심x선
        qp.drawLine(self.M2P(-100, 0), self.M2P(100, 0)) #중심 y선
     
        qp.drawPixmap(self.M2P(50, -50), self.car)
        
    def Target(self, x_m, y_m):
        point = QPoint()
        point.setX(int(self.center_x + y_m*self.target_factor))
        point.setY(int(self.center_y - x_m*self.target_factor))
        return point
    
    def target_lane(self,qp):
        qp.setPen(QPen(Qt.blue, 1)) 
        qp.drawLine(self.M2P(0.3, -100), self.M2P(0.3, 100)) #앞범퍼 끝단 선
        qp.drawLine(self.M2P(-6, -100), self.M2P(-6, 100)) #뒷차 범처 끝단
        
        qp.setPen(QPen(QColor('#5F6B53'), 1 ))
        qp.drawLine(self.M2P(0.3, -1), self.M2P(0.3, 0)) #자차 앞범퍼 와 1m
        qp.drawLine(self.M2P(-0.3, -1), self.M2P(-0.3, 0)) #자차 뒷범퍼 와 1m
        
        qp.setPen(QPen(QColor('#4A4A4A'), 1)) # 좌표선 
        qp.drawLine(self.M2P(-100, -1), self.M2P(100, -1)) # 자차와 1m
        
        qp.drawPixmap(self.M2P(0.4, -0.4), self.car)
        
    def draw_lane(self, qp,laneVal): #차선
        resolution = 0.5
        qp.setPen(QPen(QColor('#594605'), 1))
        for lane in laneVal:
            for x1 in list(np.arange(-100, 100, resolution)):
                x2 = x1 + resolution
                y1 = lane.a*x1**3 + lane.b*x1**2 + lane.c*x1 + lane.d
                y2 = lane.a*x2**3 + lane.b*x2**2 + lane.c*x2 + lane.d
                qp.drawLine(self.M2P(x1, y1), self.M2P(x2, y2))    
    
    def draw_objects(self, qp): #타겟
        qp.setPen(QPen(Qt.red, 8))
        
        for self.track in self.trackList:
            qp.drawPoint(self.Target(self.track.x, self.track.y))

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
        
    def setlane_left(self, leftLane):
        self.leftLane = leftLane

    def setlane_right(self, rightLane):
        self.rightLane = rightLane
    
    