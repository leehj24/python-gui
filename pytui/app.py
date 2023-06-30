import sys
from PyQt5.QtGui import *
from gui.main import *
from globalTimer import *

class MyApp(QMainWindow):

    def __init__(self):
        super().__init__()
        self.timer = gTimer()
        self.initUI()
    
    def initUI(self):
        gui = guiMain(self.timer)
        self.setCentralWidget(gui)
        self.setWindowTitle('Absolute Positioning')
        self.setGeometry(300, 50, 1000, 950)
        self.show()
        
if __name__ == '__main__':
    app = QApplication(sys.argv)
    myapp = MyApp()
    myapp.show()
    app.exec_()
