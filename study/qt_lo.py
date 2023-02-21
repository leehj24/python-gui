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
        self.setLayout(grid)
        
        trackList = [Track(10, 10), Track(50, 50)]
        
        bev = BirdEyeView()
        bev.setObject(trackList)
        grid.addWidget(bev, 0, 0)        
        
        # label1 = QLabel('x값', self)
        # label1.move(20, 20)
        # self.txt = QLineEdit(self)
        # self.txt.move(20, 40)
        # self.txt.resize(60, 25)
        
        # label2 = QLabel('y값', self)
        # label2.move(20, 70)
        # self.txt2 = QLineEdit(self)
        # self.txt2.move(20, 90)
        # self.txt2.resize(60, 25)
        
        # self.label3 = QLabel('x,y', self)
        # self.label3.move(20, 120)
        
        # # self.pixmap = QPixmap('im.png')
        # # self.img = QLabel(self)
        # # self.img.setPixmap(self.pixmap)
        # # self.img.move(400, 60)
        
        # btn1 = QPushButton('start', self)
        # btn1.move(90, 40)
        # btn1.resize(50,25)
        # btn1.clicked.connect(self.buttonClicked)
        
        # btn1 = QPushButton('dialog', self)
        # btn1.move(90, 120)
        # btn1.resize(50,25)
        # btn1.clicked.connect(self.dialog)
        
        # btn2 = QPushButton('stop', self)
        # btn2.move(90, 90)
        # btn2.resize(50,25)
        # btn2.clicked.connect(self.button_Clicked)
        
        bev = BirdEyeView()
        bev.move(400, 60)
        bev.resize(50, 50)

        self.setWindowTitle('Absolute Positioning')
        self.setGeometry(300, 300, 600, 600)
        self.show()
        
        # self.dialog =QDialog()
        
    def dialog(self):
        self.pixmap = QPixmap('im.png')
        self.img = QLabel(self.dialog)
        self.img.move(275, 275)
        self.img.setPixmap(self.pixmap)
        
        self.dialog.setWindowTitle('Dialog')
        self.dialog.setWindowModality(Qt.ApplicationModal)
        self.dialog.setGeometry(300, 300, 600, 600)
        self.dialog.show()
        
    # def paintEvent(self, e):
    #     qp = QPainter()
    #     qp.begin(self)
    #     self.draw(qp)
    #     qp.end()
        
    
    # def draw(self,qp):
    #     qp.setBrush(Qt.black)
    #     qp.setPen(QPen(QColor(255, 255, 255), 5))
    #     qp.drawRect(350, 150, 10, 10)#x,y가로,세로    
    
   
    # def buttonClicked(self):
    #         result = int((self.txt.text())+int(self.txt2.text()))
    #         self.label3.setText(result)
    
    def button_Clicked(self):
        self.img.clear()
        
    def buttonClicked(self):
        self.pixmap = QPixmap('im.png')
        self.img = QLabel(self)
        self.img.setPixmap(self.pixmap)
        self.img.move(400, 60)
              


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyApp()
    sys.exit(app.exec_())