import sys
import pandas as pd
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from test2 import *

class Track :
    def data(self):
        target = List(); target.name()
        self.x = target.list[1][3]
        self.y = target.list[1][4]
        
class MyWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.File = Track(); self.File.data()
        
        self.timer = QTimer(self) # 타이머 객체 생성
        self.timer.timeout.connect(self.update_index) # 타이머 시그널과 슬롯 연결
        self.timer.start(500)
        
        self.index = 0 # 배열의 인덱스
        self.initUI()
        
    def initUI(self):
        self.setGeometry(300, 300, 500, 500)
        self.setWindowTitle('Timer and Painter')
        self.show()
    
    def paintEvent(self, e):
        qp = QPainter(self) # QPainter 객체 생성
        self.target_lane(qp)
        qp.end()
        
    def target_lane(self, qp):
        qp.setPen(QPen(Qt.red,  8))
        
        qp.setPen(QPen(Qt.blue,  8))
        qp.drawPoint(self.File.x[self.index],self.File.y[self.index])
            
    def update_index(self): # 타이머 시그널에 연결된 슬롯 정의
        if self.index < len(self.File.x) : # 배열의 마지막 요소가 아니라면
            self.index += 1 # 인덱스 증가
            if self.index >= len(self.File.x):
                self.index =0
            self.update() # 화면 업데이트
        
if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = MyWidget()
    sys.exit(app.exec_())