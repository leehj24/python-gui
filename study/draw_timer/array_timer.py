import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

class Track:
    def __init__(self, x, y):
        self.x = x
        self.y = y
class MyWidget(QWidget):
    
    array = [Track(10, 10), Track(300, 50), Track(100, 100),Track(200, 10), Track(150, 50), Track(30, 100),
             Track(150, 300), Track(50, 50), Track(450, 450),Track(250, 40), Track(50, 450), Track(30, 100)]
    
    def __init__(self):
        super().__init__()
        self.timer = QTimer(self) # 타이머 객체 생성
        self.timer.timeout.connect(self.update_index) # 타이머 시그널과 슬롯 연결
        # self.timer.timeout.connect(self.updatetime)
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
        
        # for self.track in self.array:
            # qp.drawPoint(self.track.x, self.track.y) 
            # 배열의 인덱스에 해당하는 점 그리기
            # print(self.array[self.index] ,'track')
        
        for i in range(11):
            # if i >=12:
            #     self.timer = QTimer(self) # 타이머 객체 생성
            #     self.timer.start(10000)
            #     return
            for self.track in self.array:
                self.array[i] = self.array[i+1]
                qp.setPen(QPen(Qt.blue,  8))
                qp.drawPoint(self.track.x, self.track.y)
                # self.update()
                # print(self.array[i],'list',i)
                # print(self.track.x[30])
            
    def update_index(self): # 타이머 시그널에 연결된 슬롯 정의
        if self.index < len(self.array) - 1: # 배열의 마지막 요소가 아니라면
            self.index += 1 # 인덱스 증가
            self.update() # 화면 업데이트
            
    # def updatetime(self): # 타이머 시그널에 연결된 슬롯 정의
    #     if self.array.index < len(self.array) - 1: # 배열의 마지막 요소가 아니라면
    #         self.array.index += 1 # 인덱스 증가'
    #         print(self.array.index,'index')
    #         # for i in range(5):
    #         #     print(Track[i])
    #         self.update() # 화면 업데이트
            
    def setTrackList(self, array):
        self.array = array
        
if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = MyWidget()
    sys.exit(app.exec_())