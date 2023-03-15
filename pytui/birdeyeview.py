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
    # leftLane = [Lane(0,0,0,0)]
    # rightLane = [Lane(0,0,0,0)]

    def __init__(self):
        super().__init__()
        self.x = 0
        self.y = 0
        
        self.label = QLabel()
        self.canvas = QPixmap(500, 500)
        self.canvas.fill(QColor('black'))
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
        # self.draw_lane(qp)
        # self.draw_Lane(qp)

        qp.drawPixmap(QRect(100, 300, 10, 30), self.car)

        qp.end()

    def draw_objects(self, qp):
        qp.setPen(QPen(Qt.red, 8))
        
        for track in self.trackList:
            qp.drawPoint(track.x, track.y)

    # def draw_lane(self, qp):
    #     #y = ax^3 + bx^2 + cx + d
    #     qp.setPen(QPen(Qt.red, 3))
    #     for lane in self.leftLane:
    #         for r in np.arange(-3, 500, 0.1):
    #             z = lane.a*r**3 + lane.b*r**2 + lane.c*r + lane.d
    #             qp.drawPoint(r,z)

    # def draw_Lane(self, qp):
    #     qp.setPen(QPen(Qt.blue, 3))
    #     for lane in self.rightLane:
    #         for r in np.arange(50, 600, 0.1):
    #             z = lane.a*r**3 + lane.b*r**2 + lane.c*r + lane.d
    #             qp.drawPoint(r,z)
                
    def update_canvas(self):
        self.label = QLabel()
        self.canvas =QPixmap('car.png')
        self.label.setPixmap(self.canvas)
            
    def setTrackList(self, trackList):
        self.trackList = trackList

    # def setLane(self, leftLane):
    #     self.leftLane = leftLane

    # def setlane(self, rightLane):
    #     self.rightLane = rightLane
