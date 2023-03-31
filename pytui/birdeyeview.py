from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5 import *
from PIL import Image
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
    
    trackList = [Track(-5, -5)]
    leftLane = [Lane(0,0,0,2000)]
    rightLane = [Lane(0,0,0,2000)]
    
    def __init__(self):
        super().__init__()
        self.x = 0
        self.y = 0
        
        self.label = QLabel()
        self.canvas = QPixmap(self.width(),self.width())
        self.canvas.fill(QColor("#000000"))
        self.label.setPixmap(self.canvas)

        self.car = QPixmap('car.png')

        self.Layout = QVBoxLayout(self)
        self.Layout.addWidget(self.label)
        self.setLayout(self.Layout)

        self.timer = QTimer(self)
        self.timer.start(30)
        self.timer.timeout.connect(self.onTimer)
        
    def onTimer(self):
        self.update()
        
    def wheelEvent(self, event: QWheelEvent): #마우스 휠 이벤트 ui 크기 변경
        if event.angleDelta().y()>=0:
            self.canvas = QPixmap(self.width(),self.width()) # ui 증가 
            self.label.setPixmap(self.canvas)
            
        if event.angleDelta().y()<0:
            self.canvas = QPixmap(self.width()-100,self.width()-100) #ui 감소
            self.label.setPixmap(self.canvas)

    def paintEvent(self, e):
        qp = QPainter(self.label.pixmap())
        qp.eraseRect(self.canvas.rect())

        self.draw_objects(qp) # object 
        self.draw_lane(qp) #왼쪽 차선
        self.draw_Lane(qp) #오른쪽 차선
    
        transform = QTransform() # self.car 좌표변환
        transform.translate(int(self.width()/2)-60,self.height()-100) #좌표위치
        transform.scale(1, 1)
        # transform.transposed(Image.FLIP_LEFT_RIGHT)
        qp.setTransform(transform)
        
        qp.drawPixmap(0,0, self.car)
        
        # qp.end()

    def draw_objects(self, qp):
        qp.setPen(QPen(Qt.red, 8))
        
        for track in self.trackList:
            transform = QTransform()
            transform.translate(int(self.width()/3), int(self.height())) # 좌표변환
            transform.rotate(270) #회전 각도
            transform.scale(1, 1)
            qp.setTransform(transform)
            qp.drawPoint(track.x, track.y)

    def draw_lane(self, qp):

        qp.setPen(QPen(Qt.blue, 3))
        for lane in self.leftLane:
            for r in list(np.arange(-500, 500, 0.1)):
                z = lane.a*r**3 + lane.b*r**2 + lane.c*r + lane.d
            
                transform = QTransform()
                transform.translate(int(self.width()/3), int(self.height()/2))
                transform.rotate(0)
                transform.scale(1, 1)
                qp.setTransform(transform)
                
                qp.drawPoint(10*r,15*z)
                
    def draw_Lane(self, qp):
        
        qp.setPen(QPen(Qt.blue, 3))
        for lane in self.rightLane:
            for r in np.arange(-500, 500, 0.1):
                z = lane.a*r**3 + lane.b*r**2 + lane.c*r + lane.d
                
                transform = QTransform()
                transform.translate(int(self.width()/2), int(self.height()/2))
                transform.rotate(270)
                transform.scale(1, 1)
                qp.setTransform(transform)
                qp.drawPoint(z,r)
            
    def setTrackList(self, trackList):
        self.trackList = trackList

    def setLane(self, leftLane):
        self.leftLane = leftLane

    def setlane(self, rightLane):
        self.rightLane = rightLane