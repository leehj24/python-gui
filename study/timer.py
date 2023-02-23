import sys

from PyQt5.QtCore import pyqtSlot, QTimer, Qt, QCoreApplication
from PyQt5.QtGui import QPainter, QPen
from PyQt5.QtWidgets import QWidget, QApplication, QPushButton


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.pos_x = 0
        self.direction = 1
        self.speed = 3

    def initUI(self):
        # 윈도우 설정
        self.setGeometry(300, 300, 300, 300)  # x, y, w, h
        self.setWindowTitle('QPaint Move')

        # 창닫기 버튼
        btn = QPushButton('stop', self)
        btn.move(1,1)
        btn.resize(btn.sizeHint())
        btn.clicked.connect(self.stop)
        
        btn2 = QPushButton('play', self)
        btn2.move(100,1)
        btn2.resize(btn.sizeHint())
        btn2.clicked.connect(self.play)

    def paintEvent(self, e):
        qp = QPainter()
        qp.begin(self)
        self.draw_point(qp)
        qp.end()

    def draw_point(self, qp):
        qp.setPen(QPen(Qt.blue, 8))
        qp.drawPoint(self.pos_x, 100)

    def timeout_run(self):
        if self.pos_x < 0 or self.pos_x > self.width() - 8:
            self.direction *= -1
        self.pos_x = self.pos_x + (self.direction * self.speed)
        print(self.pos_x, self.width())
        self.update()
        
    def stop(self):
        self.timer.stop()
        
    def play(self):
        self.timer = QTimer(self)
        self.timer.start(500)
        self.timer.timeout.connect(self.timeout_run)
        

if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.exec_())