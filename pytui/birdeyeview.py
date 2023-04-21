from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5 import *
import numpy as np
import pandas as pd
class Track:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        
        # self.data = pd.read_csv("data.csv", index_col=['x','y'], enconding ='co949')
        # self.xy = self.data['x','y']
class Lane:
    def __init__(self, a, b, c, d):
        self.a = a
        self.b = b
        self.c = c
        self.d = d
class BirdEyeView(QWidget):
    
    trackList = [Track(-400, 0)]
    leftLane = [Lane(0, 0, 0, -1)] #0.0001, 0.01, -0.174, -1.5
    rightLane = [Lane(0, 0, 0, 1)] #0.0001, 0.01, -0.174, 1.5
    scale_factor = 50 #그리드 사이즈 증가
    scale_factor2 = 1
    
    def __init__(self):
        super().__init__()

        self.setLayout(QHBoxLayout())
        self.label = QLabel()
        self.canvas = QPixmap(self.width(),self.width())
        self.canvas.fill(Qt.black)
        self.label.setPixmap(self.canvas)

        self.car = QPixmap('car.png')
        
        self.UpdateWidget = QWidget()
        self.UpdateWidget.setLayout(QVBoxLayout())
        self.UpdateWidget.layout().addWidget(QSizeGrip(self))
        self.UpdateWidget.layout().addWidget(self.label)

        self.layout().addWidget(self.UpdateWidget)
        
        # self.Layout = QVBoxLayout(self)
        # self.Layout.addWidget(self.label,0)
         # self.sizegrip = QSizeGrip(self)
        # self.Layout.addWidget(self.sizegrip,1)
        
        # self.layout().setSpacing(0)
        # self.layout().setContentsMargins(0,0,0,0)
        # self.UpdateWidget.layout().setSpacing(4)
        # self.UpdateWidget.layout().setContentsMargins(0,0,0,0)
        
        # self.setLayout(self.Layout)

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

        self.draw_grid(qp)
        
        self.draw_objects(qp) # object 
        self.draw_lane(qp, self.leftLane) #왼쪽 차선
        self.draw_lane(qp, self.rightLane) #오른쪽 차선
        
        qp.end()

    def M2P(self, x_m, y_m):
        point = QPoint()
        point.setX(int(self.center_x + y_m*self.scale_factor))
        point.setY(int(self.center_y - x_m*self.scale_factor))
        return point
    
    def Target(self, x_m, y_m):
        point = QPoint()
        point.setX(int(self.center_x + y_m*self.scale_factor2))
        point.setY(int(self.center_y - x_m*self.scale_factor2))
        return point
    
    def UPC(self):
        
        label2 = QLabel()
        up_canvas2 = QPixmap()
        up_canvas2.width(int( self.canvas_x1))
        up_canvas2.height(int(self.canvas_y1))
        self.canvas2.fill(Qt.black)
        label2.setPixmap(up_canvas2)
        return up_canvas2
        
    def wheelEvent(self, event: QWheelEvent): #마우스 휠 이벤트 ui 크기 변경
        # print(self.canvas_x)
        if event.angleDelta().y()>=0:
            painter = QPainter(self) # ui 증가 
            painter.drawPixmap(self.UPC(10,10),self.UPC(10,10))
    
        if event.angleDelta().y()<0:
            self.canvas = QPixmap(self.UPC(10,10),self.UPC(10,10)) #ui 감소
            self.label.setPixmap(self.canvas)
            
    # def wheelEvent(self,label): #마우스 휠 이벤트 ui 크기 변경
    #     wheel = QWheelEvent
    #     if wheel.angleDelta().y()>=0:
    #         label.drawPixmap(self.UPC(-100, 0)) # ui 증가 
    #     if wheel.angleDelta().y()<0:
    #         label.drawPixmap(self.UPC(-100, 0)) # ui 증가 
    
    def upgrade(self,event=QMouseEvent):
        if event.buttons() & Qt.LeftButton:
            canvas = QPixmap(self.UPC(100,100),self.UPC(100,100))
            canvas.fill(Qt.black)
            self.label.setPixmap(canvas)
    
    def draw_grid(self, qp):
    
        qp.setPen(QPen(QColor('#4A4A4A'), 1))
        for x_1 in range(-100,100):
            for y_1 in range(-100,100):
                qp.drawLine(self.M2P(x_1, y_1), self.M2P(x_1, -y_1)) # y선
                qp.drawLine(self.M2P(-x_1, y_1), self.M2P(x_1, y_1)) # x선
                
        qp.setPen(QPen(Qt.gray, 1))
        qp.drawLine(self.M2P(0, -100), self.M2P(0, 100))
        qp.drawLine(self.M2P(-100, 0), self.M2P(100, 0))
        
        qp.drawPixmap(self.M2P(0.4, -0.4), self.car)

            
    def draw_objects(self, qp):
        qp.setPen(QPen(Qt.red, 8))
        
        for track in self.trackList:
            qp.drawPoint(self.Target(track.x, track.y))

    def draw_lane(self, qp,laneVal):
        resolution = 0.5
        qp.setPen(QPen(Qt.yellow, 1))
        for lane in laneVal:
            for x1 in list(np.arange(-100, 100, resolution)):
                x2 = x1 + resolution
                y1 = lane.a*x1**3 + lane.b*x1**2 + lane.c*x1 + lane.d
                y2 = lane.a*x2**3 + lane.b*x2**2 + lane.c*x2 + lane.d
                qp.drawLine(self.M2P(x1, y1), self.M2P(x2, y2))
            
    def setTrackList(self, trackList):
        self.trackList = trackList

    def setlane_left(self, leftLane):
        self.leftLane = leftLane

    def setlane_right(self, rightLane):
        self.rightLane = rightLane