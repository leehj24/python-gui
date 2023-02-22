import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import pandas as pd

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
        
        self.timer = QTimer(self)
        self.timer.start(30)
        self.timer.timeout.connect(self.timeout_run)
        
    # def timeout_run(self):
    #     i=0
    #     for i in self.trackList[i]:
    #         i =  i+1
    #     self.update()
               
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
        
        trackList = [Track(10, 10), Track(50, 50), Track(80,80)]
        
        bev = BirdEyeView()
        bev.setObject(trackList)
        grid.addWidget(bev, 0, 1) 
        
        self.lb = QLabel(self)
        
        grid.addWidget(self.firstGroup(), 0, 0)
        grid.addWidget(self.secondGroup(), 1, 0)
        grid.addWidget(self.thirdGroup(), 2, 0)
        grid.addWidget(self.lb, 3, 0)
        grid.addWidget(QTextBrowser(), 2, 1) #QScrollArea
              
        self.setLayout(grid)
        grid = QGridLayout()
        
        self.setWindowTitle('Absolute Positioning')
        self.setGeometry(300, 300, 700, 600)
        self.show()
        
    def firstGroup(self):
        groupbox = QGroupBox('데이터')
        
        label1 = QLabel('x값', self)
        label2 = QLabel('y값', self)
        txt = QLineEdit(self)
        
        txt2 = QLineEdit(self)
        txt2.resize(60, 25)
        
        vbox = QVBoxLayout()
        vbox.addWidget(label1)
        vbox.addWidget(txt)
        txt.resize(60, 25)
        vbox.addWidget(label2)
        vbox.addWidget(txt2)
        groupbox.setLayout(vbox)

        return groupbox
    
    def secondGroup(self):
        groupbox = QGroupBox('데이터')
        
        btn1 = QPushButton('start', self)
        btn1.clicked.connect(self.buttonClicked)
        
        btn2 = QPushButton('dialog', self)
        btn2.clicked.connect(self.dialog)
        
        btn3 = QPushButton('stop', self)
        btn3.clicked.connect(self.bt_stop)
        
        btn4 = QPushButton('play', self)
        btn4.clicked.connect(self.bt_play)
        
        vbox = QVBoxLayout()
        vbox.addWidget(btn1)
        vbox.addWidget(btn2)
        vbox.addWidget(btn3)
        vbox.addWidget(btn4)
        groupbox.setLayout(vbox)
        
        return groupbox
    
    #https://hongsusoo.github.io/angleprice_1/
    def thirdGroup(self):
        groupbox = QGroupBox('테이블')
        self.tableWidget = QTableWidget()
        self.tableWidget.setRowCount(2)
        self.tableWidget.setColumnCount(2)
        self.tableWidget.setItem(0,0,QTableWidgetItem('Apple'))
        
        layout = QVBoxLayout()
        layout.addWidget(self.tableWidget)
        groupbox.setLayout(layout)
        return groupbox
    
    def bt_play(self):
        self.timer = QTimer(self)
        self.timer.start(50)
        self.timer.timeout.connect(self.timeout_run)
    
    def timeout_run(self):
        i=0
        for i in self.trackList:
            i =  i+1
            if i < 100:
                continue
        self.update()
    
    def bt_stop(self):
        self.timer.stop()
    
    def buttonClicked(self):
        self.lb.setText('self.x,y')
        
    def dialog(self):
        d= QDialog
        d.setWindowTitle('Dialog')
        d.setWindowModality(Qt.ApplicationModal)
        d.setGeometry(300, 300, 700, 700)
        d.show()
    
        
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyApp()
    sys.exit(app.exec_())