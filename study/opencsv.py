# import pandas as pd
# from matplotlib import pyplot as plt
# bb_data = pd.read_csv('data.csv')
# plt.plot(bb_data.num, bb_data.a)
# plt.show()

import sys
import pandas as pd
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import matplotlib.pyplot as plt


class Main(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        #불러올 파일 형식(excel or csv) 선택 창
        btnload = QPushButton('select_file', self)
        btnload.clicked.connect(self.fileopenActivated)
       
        self.setGeometry(300, 300, 600, 600)  # x, y, w, h
        self.setWindowTitle('QPaint Move')
        
    #위치 결정
        hbox_1 = QHBoxLayout()
        hbox_1.addWidget(btnload)
        self.setLayout(hbox_1)  
        self.show()

    def fileopenActivated(self): #파일 형식 선택 
        a = QFileDialog.getOpenFileName(self)         
        self.data = pd.read_csv(a[0])
        print(self.data)
        plt.plot(self.data.num, self.data.a)
        plt.plot(self.data.num, self.data.a1)
        plt.show()
      
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Main()
    sys.exit(app.exec_())