from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5 import *
from gui.birdeyeview import *
from gui.select_file import *
from globalTimer import *

class guiMain(QScrollArea):
    
    trackList = [Track(-300, -30)]
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
        grid = QGridLayout()
        grid.addWidget(self.firstGroup(),0,0)
        grid.addWidget(self.secondGroup(),1,0)
   
        widget = QWidget()
        widget.setLayout(grid)

        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.setWidgetResizable(True)
        self.setWidget(widget)
        
    def firstGroup(self):
        groupbox = QGroupBox('파일')
        self.btn = QPushButton('RUN', self)
        self.btn.setCheckable(True)
        self.btn.clicked.connect(self.play)
        
        self.btn2 = QPushButton('STOP', self)
        self.btn2.clicked.connect(self.stop)
        
        file = Openfile()
        hbox = QHBoxLayout()
        hbox.addWidget(file)
        hbox.addWidget(self.btn)
        hbox.addWidget(self.btn2)
        groupbox.setLayout(hbox)
        return groupbox
    
    def secondGroup(self):
        groupbox = QGroupBox('BirdEyeView')
        self.bev = BirdEyeView()
        
        self.step = 0
        self.slider = QSlider(Qt.Horizontal, self)
        self.slider.valueChanged.connect(self.slider.setValue)
        
        vbox = QVBoxLayout()
        vbox.addWidget(self.bev)
        vbox.addWidget(self.slider)
        groupbox.setLayout(vbox)
        return groupbox
        
    def timeout_run(self):
        if self.isStart:
            for self.track in self.trackList:
                self.track.x = self.track.x + 1
            print(self.trackList)
            self.bev.setTrackList(self.trackList)
            self.bev.setlane_left(self.leftLane)
            self.bev.setlane_right(self.rightLane)
             
            if self.step >= 100:
                self.step=0
                return
            
            self.step = self.step + 0.5
            self.slider.setValue(int(self.step))
            
    def play(self):
        self.gtimer.start()

        self.btn.setCheckable(True)
        
        if not self.isStart:
            self.timer = QTimer(self)
            self.timer.start(100)
            self.timer.timeout.connect(self.timeout_run)
            self.isStart = True
            
        if self.btn.isChecked():
            self.btn.setText('Pause')
            
        else:
            self.btn.setText('RUN')
            self.timer.stop()
            self.isStart = False
            
    def stop(self):
        self.btn.setCheckable(False)
        
        self.timer.stop()
        self.isStart = False
        self.btn.setText('RUN')
        self.btn.setCheckable(True)
        self.trackList = [Track(-300, -30)]
        
    # def closeEvent(self, event):
    #     self.saveSetting()
    #     super(guiMain,self).closeEvent(event)
        
    # def saveSetting(self):
    #     settings = QSettings('myorg')