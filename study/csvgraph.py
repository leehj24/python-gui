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
        
class BirdEyeView(QMainWindow):
    
    trackList = [Track(-5, -5)]

    def __init__(self):
        super().__init__()
        self.x = 0
        self.y = 0
        
        self.label = QLabel()
        self.canvas =QPixmap('car.png')
        self.label.setPixmap(self.canvas)
        widget = QWidget()
        
        # vbox = QVBoxLayout(widget)
        # vbox.addWidget(self.label)
        self.setCentralWidget(widget)
        
    def paintEvent(self, e):
        qp = QPainter(self.label.pixmap())
        self.timer = QTimer(self)
        self.timer.start(50)
        self.timer.timeout.connect(self.update_canvas)
        
        # qp.begin(self)      -painter already active 로그창 
        self.draw_objects(qp)
        # qp.end()
        # self.update()

    def draw_objects(self,qp):
        qp.setPen(QPen(Qt.yellow, 8))
        
        for track in self.trackList:
            qp.drawPoint(track.x, track.y)
            
    def update_canvas(self):
        self.label = QLabel()
        self.canvas =QPixmap('car.png')
        self.label.setPixmap(self.canvas)
        widget = QWidget()
        
        vbox = QVBoxLayout(widget)
        vbox.addWidget(self.label)
        self.setCentralWidget(widget)
            
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
        
        grid.addWidget(self.firstGroup(), 1, 0) #x,y,데이터
        grid.addWidget(self.secondGroup(), 2, 0)# 버튼
        grid.addWidget(self.thirdGroup(), 0, 0)#테이블
        grid.addWidget(self.lb, 3, 0)
        grid.addWidget(self.fourGroup(), 1, 1)#그래프
        # grid.addWidget(QScrollArea(), 2, 1) #QTextBrowser
              
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
        
        btn3 = QPushButton('play', self)
        btn3.clicked.connect(self.play)
        
        btn4 = QPushButton('stop', self)
        btn4.clicked.connect(self.stop)
        
        vbox = QVBoxLayout()
        vbox.addWidget(btn1)
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
    
    def fourGroup(self):
        groupbox = QGroupBox('그래프')
        btnload = QPushButton('select_file', self)
        # plot_widget = pg.PlotWidget()
        self.listwidget_01 = QListWidget(self)
        self.listwidget_01.setToolTip('불러온 파일의 컬럼명을 보여줍니다.')
        
        btnload.clicked.connect(self.button_graph)
        self.listwidget_01.itemDoubleClicked.connect(self.doubleclicked_listwidget)
        self.listwidget_01.itemDoubleClicked.connect(self.graphplot)
        
        vbox = QVBoxLayout()
        vbox.addWidget(btnload)
        # vbox.addWidget(plot_widget)
        vbox.addWidget(self.listwidget_01)
        groupbox.setLayout(vbox)
        return groupbox
    
    def button_graph(self):
        fname = QFileDialog.getOpenFileName(self, 'Open file', './')
        self.data = []
        self.listwidget_01.clear()
        try:
            self.data=pd.read_csv(fname[0], index_col=0)
            i = 1      
            for i in range(len(self.data.columns)):
              temp_Item = QListWidgetItem(self.data.columns[i])
              self.listwidget_01.addItem(temp_Item)

        except ValueError:
            QMessageBox.warning(self, '형식이 일치하지 않습니다.', '형식이 일치하는 파일을 불러오시오')     

        except FileNotFoundError:
            QMessageBox.warning(self, '파일이 없습니다.', '형식에 맞는 파일을 선택하시오')
        
    def doubleclicked_listwidget(self): #그리고자 하는 column을 선택
        list_item = self.listwidget_01.selectedItems()

        for item in list_item:
            self.listwidget_01.addItem(item)    
            
    def graphplot(self):
        num = 0
        num = self.listwidget_01.count()
        sel_culm = []                         
        new_data = pd.DataFrame()            
        selection = []
        if num == 0:
            plt.close()
            
        for i in range(0,num):
            selection = self.listwidget_01.item(i)
            sel_culm = selection.text()          
            if sel_culm in self.data.columns:
                new_data[sel_culm] = self.data[sel_culm]

            plt.close()
            plt.plot(new_data, label=new_data.columns)
            # plt.xticks(rotation=30)
            # plt.margins(x=0,y=0)
            legend = plt.legend()    
            legend.set_draggable(True) 
            plt.grid(True)#격자
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

    def buttonClicked(self):
        self.lb.setText('self.x,y')
        
        
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
     
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyApp()
    ex.show()
    app.exec_()
    # sys.exit(app.exec_())