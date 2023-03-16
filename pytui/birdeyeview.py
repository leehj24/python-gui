from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5 import *
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
    leftLane = [Lane(0,0,0,0)]
    # rightLane = [Lane(0,0,0,0)]

    def __init__(self):
        super().__init__()
        self.x = 0
        self.y = 0
        
        self.label = QLabel()
        self.canvas = QPixmap(self.width(),self.height())
        self.canvas.fill(QColor("black"))
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

    def paintEvent(self, e):
        qp = QPainter(self.label.pixmap())

        qp.eraseRect(self.canvas.rect())

        self.draw_objects(qp)
        self.draw_lane(qp)
        # self.draw_Lane(qp)
        
        qp.drawPixmap(300, 400, self.car)

        qp.end()

    def draw_objects(self, qp):
        qp.setPen(QPen(Qt.red, 8))
        
        for track in self.trackList:
            qp.drawPoint(track.x, track.y)

    def draw_lane(self, qp):
        qp.setPen(QPen(Qt.red, 3))
        for lane in self.leftLane:
            for x in np.arange(-3, 500, 1):
                y = lane.a*x**3 + lane.b*x**2 + lane.c*x + lane.d
                qp.drawPoint(x,y)
                
    # def draw_Lane(self, qp):
    #     qp.setPen(QPen(Qt.red, 3))
        # for lane in self.leftLane:
        #     for x in np.arange(-3, 500, 1):
        #         y = lane.a*x**3 + lane.b*x**2 + lane.c*x + lane.d
        #         qp.drawPoint(x,y)
            

    def setTrackList(self, trackList):
        self.trackList = trackList

    def setLane(self, leftLane):
        self.leftLane = leftLane

    # def setlane(self, rightLane):
    #     self.rightLane = rightLane