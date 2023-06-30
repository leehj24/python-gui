from PyQt5.QtCore import *

class gTimer(QObject):

    timeout = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.isStart = False

    def start(self):
        if not self.isStart:
            self.timer = QTimer(self)
            self.timer.start(10)
            self.timer.timeout.connect(self.onTimer)
            self.isStart = True

    def onTimer(self):
        self.timeout.emit()