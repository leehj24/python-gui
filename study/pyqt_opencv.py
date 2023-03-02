import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from pandas import *
import pandas as pd
import matplotlib.pyplot as plt
import pyqtgraph as pg

class Track:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        
class BirdEyeView(QWidget):
    
    trackList = [Track(0, 0)]

    def __init__(self):
        super().__init__()
        self.x = 0
        self.y = 0
                
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

        grid.addWidget(self.bev, 0, 1) 
        
        self.lb = QLabel(self)
        
        grid.addWidget(self.firstGroup(), 0, 0)
        grid.addWidget(self.secondGroup(), 1, 0)
        grid.addWidget(self.thirdGroup(), 2, 0)
        grid.addWidget(self.lb, 3, 0)
        # grid.addWidget(self.fourGroup(), 2, 1)
        grid.addWidget(QScrollArea(), 2, 1) #QTextBrowser
              
        self.setLayout(grid)
        grid = QGridLayout()
        
        self.setWindowTitle('Absolute Positioning')
        self.setGeometry(300, 100, 1000, 800)
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
        groupbox = QGroupBox('버튼')
        
        btn1 = QPushButton('click', self)
        btn1.clicked.connect(self.buttonClicked)
        
        # btn2 = QPushButton('dialog', self)
        # btn2.clicked.connect(self.dialog)
        
        btn2 = QPushButton('select_csv', self)
        btn2.clicked.connect(self.select_csv)
        # btn2.clicked.connect(self.button_load)
        
        btn3 = QPushButton('play', self)
        btn3.clicked.connect(self.play)
        
        btn4 = QPushButton('stop', self)
        btn4.clicked.connect(self.stop)
        
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
        table = QTableWidget()
        btn_load = QPushButton('load', self)
        btn_load.clicked.connect(lambda state, widget = table: self.button_load(state, widget))
        layout = QVBoxLayout()
        layout.addWidget(table)
        layout.addWidget(btn_load)
        groupbox.setLayout(layout)
        return groupbox

    def buttonClicked(self):
        self.lb.setText('self.x,y')
        
    # def dialog(self):
    #     d= QDialog
    #     d.setWindowTitle('Dialog')
    #     d.setWindowModality(Qt.ApplicationModal)
    #     d.setGeometry(300, 300, 700, 700)
    #     d.show()
        
    def timeout_run(self):
        for track in self.trackList:
            track.x = track.x + 1
            
        self.bev.setTrackList(self.trackList)

    def play(self):
        self.timer = QTimer(self)
        self.timer.start(30)
        self.timer.timeout.connect(self.timeout_run)

    def stop(self):
        self.timer.stop()       
        
     # def fourGroup(self):
    #     groupbox = QGroupBox('그래프')
    #     return groupbox
        
    def select_csv(self):
        a = QFileDialog.getOpenFileName(self)         
        data = pd.read_csv(a[0])
        plt.plot(data.num, data.a)
        plt.plot(data.num, data.a1)
        plt.plot(data.num, data.b)
        plt.plot(data.num, data.b1)
        # print (data)
        plt.show()

    def button_load(self, state, widget):
        filename = QFileDialog.getOpenFileName(self, 'Open file', './')
    
        if filename[0]:
            df = pd.read_csv(filename[0], index_col = 0)
            self.create_table_widget(widget, df)
            
    def create_table_widget(self, widget, df):
        widget.setRowCount(len(df.index))
        widget.setColumnCount(len(df.columns))
        widget.setHorizontalHeaderLabels(df.columns)
        widget.setVerticalHeaderLabels(df.index)

        for row_index, row in enumerate(df.index):
            for col_index, column in enumerate(df.columns):
                value = df.loc[row][column]
                item = QTableWidgetItem(str(value))
                widget.setItem(row_index, col_index, item)      
     
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyApp()
    sys.exit(app.exec_())