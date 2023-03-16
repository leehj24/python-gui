import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout
from PyQt5.QtGui import QPainter, QBrush, QPen
from PyQt5.QtCore import Qt

class Canvas(QWidget):
    def __init__(self, parent=None):
        super(Canvas, self).__init__(parent)
        self.setAutoFillBackground(True)
    
    def paintEvent(self, event):
        qp = QPainter()
        qp.begin(self)
        self.draw(qp)
        qp.end()
    
    def draw(self, qp):
        brush = QBrush(Qt.SolidPattern)
        qp.setBrush(brush)
        qp.drawRect(0, 0, self.width()-1, self.height()-1)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
    
    def initUI(self):
        self.setWindowTitle('PyQt Canvas Example')
        self.resize(500, 500)
        
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        vbox = QVBoxLayout()
        central_widget.setLayout(vbox)
        
        self.canvas = Canvas(self)
        vbox.addWidget(self.canvas)
        
        self.show()
    
    def resizeEvent(self, event):
        self.canvas.resize(self.width(), self.height())

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec_())