import sys
from PyQt5.QtWidgets import *


class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.resize(400, 200)
        
        self.btn = QPushButton("종료", self)
        self.btn.move(20, 20)
        self.btn.resize(300,30)#버튼사이즈
        self.btn.clicked.connect(self.btn_clicked)

    # 버튼이 클릭될 때 호출되는 메서드
    def btn_clicked(self):
        self.close()


app = QApplication(sys.argv)
mywindow = MyWindow()
mywindow.show()
app.exec_()