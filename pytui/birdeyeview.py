from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5 import *

class Track:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class Lane:
    def __init__(self, a, b, c, d):
        self.a = a


class BirdEyeView(QWidget):
    
    trackList = [Track(-5, -5)]

    def __init__(self):
        super().__init__()
        self.x = 0
        self.y = 0
        
        self.label = QLabel()
        self.canvas = QPixmap(400, 300)
        self.canvas.fill(Qt.white)
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

        qp.drawPixmap(QRect(10, 10, 10, 30), self.car)

        qp.end()

    def draw_objects(self, qp):
        qp.setPen(QPen(Qt.red, 8))
        
        for track in self.trackList:
            qp.drawPoint(track.x, track.y)

    def draw_lane(self, qp):
        #y = ax^3 + bx^2 + cx + d
        for x in range(0, 50, 0.1):
            y = self.leftLane.a*x*x*x + self.leftLane.b*x*x + self.leftLane.c*x + self.leftLane.d
            qp.drawPoint
            
    def update_canvas(self):
        self.label = QLabel()
        self.canvas =QPixmap('car.png')
        self.label.setPixmap(self.canvas)
            
    def setTrackList(self, trackList):
        self.trackList = trackList

    def setLane(self, leftLane, rightLane):
        self.leftLane = leftLane
        self.rightLane = rightLane
