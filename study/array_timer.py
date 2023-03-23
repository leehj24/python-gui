import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

class MyWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.timer = QTimer(self) # 타이머 객체 생성
        self.timer.timeout.connect(self.update_index) # 타이머 시그널과 슬롯 연결
        self.timer.start(1000)
        # self.timer.setInterval(6000) # 타이머 간격 설정 (1000ms = 1s)
        self.array = [(10, 10), (300, 50), (100, 100),(200, 10), (150, 50), (30, 100),
                      (150, 300), (50, 50), (450, 450),(250, 40), (50, 450), (30, 100)] # 점의 좌표를 담은 배열
        self.index = 0 # 배열의 인덱스
        self.initUI()

    def initUI(self):
        self.setGeometry(300, 300, 500, 500)
        self.setWindowTitle('Timer and Painter')
        self.show()
    
    def paintEvent(self, e):
        qp = QPainter(self) # QPainter 객체 생성
        qp.setPen(QPen(Qt.blue,  8))
        qp.drawPoint(*self.array[self.index]) # 배열의 인덱스에 해당하는 점 그리기
    
    def update_index(self): # 타이머 시그널에 연결된 슬롯 정의
        if self.index < len(self.array) - 1: # 배열의 마지막 요소가 아니라면
            self.index += 1 # 인덱스 증가
            self.update() # 화면 업데이트
            
if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = MyWidget()
    sys.exit(app.exec_())