import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

class BirdEyeView(QWidget):
    
    def __init__(self):
        super().__init__()
        self.x = 50
        self.y = 50

    def paintEvent(self, e):
        qp = QPainter()
        qp.begin(self)
        self.draw_objects(qp)
        qp.end()
        self.update()
        
    def draw_objects(self, qp):
        qp.setPen(QPen(Qt.blue, 8))
        for track in self.trackList:
            qp.drawPoint(track.x, track.y)
        
    def setObject(self, trackList):  
        self.trackList = trackList

class Track:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class MyApp(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        grid = QGridLayout()
        
        trackList = [Track(10, 10), Track(50, 50)]
        
        bev = BirdEyeView()
        bev.setObject(trackList)
        grid.addWidget(bev, 0, 1) 
        grid.addWidget(self.firstGroup(), 0, 0)
        
        grid.addWidget(QLabel('x값'), 1, 0)
        grid.addWidget(QLineEdit(), 2, 0)
        grid.addWidget(QLabel('y값'), 3, 0)
        grid.addWidget(QLineEdit(), 4, 0) 
        grid.addWidget(QLineEdit(), 4, 1)
        grid.addWidget(QLineEdit(), 5, 2)
              
        self.setLayout(grid)
        bev = BirdEyeView()
        # bev.move(400, 60)
        # bev.resize(50, 50)
        
        self.setWindowTitle('Absolute Positioning')
        self.setGeometry(300, 300, 600, 600)
        self.show()
        
    def firstGroup(self):
        groupbox = QGroupBox('데이터')
        
        label1 = QLabel('x값', self)
        label2 = QLabel('y값', self)
        txt = QLineEdit(self)
        txt.resize(60, 25)
        txt2 = QLineEdit(self)
        txt2.resize(60, 25)
        
        vbox = QVBoxLayout()
        vbox.addWidget(label1)
        vbox.addWidget(label2)
        vbox.addWidget(txt)
        vbox.addWidget(txt2)
        groupbox.setLayout(vbox)

        return groupbox
    
       
        
        
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyApp()
    sys.exit(app.exec_())