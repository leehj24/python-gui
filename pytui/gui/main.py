from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5 import *
from gui.birdeyeview import *
from gui.select_file import *
class guiMain(QScrollArea):
    
    trackList = Track()  #; trackList.data()
    leftLane = [Lane(0, 0, 0, -0.5)]
    rightLane = [Lane(0, 0, 0, 0.5)]
  
    @pyqtSlot()
    def onUpdateData(self):
        # print("onTimer")
        pass

    def __init__(self, gtimer):
        super().__init__()
        self.isStart = False 
        self.gtimer = gtimer
        self.initUI()

        self.gtimer.timeout.connect(self.onUpdateData)
 
    def initUI(self):
        self.bev = BirdEyeView()
        vbox = QVBoxLayout()
        vbox.addWidget(self.bev)
        widget = QWidget()
        widget.setLayout(vbox)

        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.setWidgetResizable(True)
        self.setWidget(widget)