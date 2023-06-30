import sys
import pandas as pd
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

df =  pd.read_csv('./data.csv')
x= df.loc[:,'x']
y= df.loc[:,'y']
        
class MyWidget(QWidget):
    def __init__(self):
        super().__init__()
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
            
        for i in range(len(x)):
            qp.setPen(QPen(Qt.blue,  8))
            print(x[i],y[i])
            qp.drawPoint(x[i],y[i])
            
    # def setTrackList(self, array):
    #     self.array = array
        
if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = MyWidget()
    sys.exit(app.exec_())