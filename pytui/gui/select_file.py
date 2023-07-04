import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import json
class Openfile(QWidget):
    
    def __init__(self):
        super().__init__()
        self.initUI()
        
    def initUI(self):
        self.OEM=QComboBox()
        file_path = "./config/oem.json"
        with open(file_path) as file:
            data = json.load(file)
            self.json_test = data['OEM']
        
        for k in self.json_test:
            self.O_Name= k['name']
            self.OEM.addItem(self.O_Name)
        self.settings = QSettings('MyQtApp','myorg')
        self.OEM.setCurrentText(self.settings.value('OEM'))
        self.OEM.activated[str].connect(self.fileopenActivated)
        
        self.vehicle1=QComboBox()
        self.scenario=QComboBox()
        
        if self.OEM.currentText() == 'HKMC':
            for i in range(0,2):
                V_name = self.json_test[0]['vehicles'][i]['name']
                self.vehicle1.addItem(V_name)
            self.vehicle1.setCurrentText(self.settings.value('vehicles'))
            
        if self.vehicle1.currentText() == 'RG3':
            self.scenario.addItem(self.json_test[0]['vehicles'][0]['can1'])
            self.scenario.addItem(self.json_test[0]['vehicles'][0]['can2'])
            self.scenario.setCurrentText(self.settings.value('scenario'))
            
        elif self.vehicle1.currentText() == 'RS4':
            self.scenario.addItem(self.json_test[0]['vehicles'][1]['can1'])
            self.scenario.addItem(self.json_test[0]['vehicles'][1]['can2'])
            self.scenario.setCurrentText(self.settings.value('scenario'))
        
        Hbox1 = QHBoxLayout()
        Hbox1.addWidget(QLabel('OEM'))
        Hbox1.addWidget(self.OEM)
        
        Hbox1.addWidget(QLabel('차량'))
        Hbox1.addWidget(self.vehicle1)
        self.vehicle1.setFixedSize(100,25)
        self.vehicle1.activated[str].connect(self.fileopenActivated1)
        
        Hbox1.addWidget(QLabel('시나리오'))
        Hbox1.addWidget(self.scenario)
        self.scenario.setFixedSize(300,25)
        self.setLayout(Hbox1)
        
    def fileopenActivated(self,text):
        self.saveSetting()
        if text == 'HKMC':
            self.vehicle1.clear()
            self.scenario.clear()
            for i in range(0,2):
                V_name = self.json_test[0]['vehicles'][i]['name']
                self.vehicle1.addItem(V_name)
        elif text == 'SYMC':
            self.vehicle1.clear()
            self.scenario.clear()
            # for i in range(0,2):
            #     V_name = self.json_test[1]['vehicles'][i]['name']
            #     self.vehicle1.addItem(V_name)
        elif text == 'LUCID':
            self.vehicle1.clear()
            self.scenario.clear()
            # for i in range(0,2):
            #     V_name = self.json_test[2]['vehicles'][i]['name']
            #     self.vehicle1.addItem(V_name)
        else:
            self.vehicle1.clear()
            self.scenario.clear()
            # for i in range(0,2):
            #     V_name = self.json_test[3]['vehicles'][i]['name']
            #     self.vehicle1.addItem(V_name)
        
    def fileopenActivated1(self,text):
        self.saveSetting()
        
        self.scenario.setCurrentText(self.settings.value('scenario'))
        if text == 'RG3':
            self.scenario.clear()
            self.scenario.addItem(self.json_test[0]['vehicles'][0]['can1'])
            self.scenario.addItem(self.json_test[0]['vehicles'][0]['can2'])
          
        elif text == 'RS4':
            self.scenario.clear()
            self.scenario.addItem(self.json_test[0]['vehicles'][1]['can1'])
            self.scenario.addItem(self.json_test[0]['vehicles'][1]['can2'])
            
        # elif text == 'name1':
        #     self.scenario.clear()
        #     self.scenario.addItem(self.json_test[1]['vehicles'][0]['can1'])
        #     self.scenario.addItem(self.json_test[1]['vehicles'][0]['can2'])
     
        # elif text == 'name2':
        #     self.scenario.clear()
        #     self.scenario.addItem(self.json_test[1]['vehicles'][1]['can1'])
        #     self.scenario.addItem(self.json_test[1]['vehicles'][1]['can2'])
    
    def closeEvent(self, event):
        self.saveSetting()
        super(Openfile,self).closeEvent(event)
        print(self.OEM.currentText())
        print(self.vehicle1.currentText())
        print(self.scenario.currentText())

    def saveSetting(self):
        self.settings = QSettings('MyQtApp','myorg')
        self.settings.setValue('OEM',self.OEM.currentText())
        self.settings.setValue('vehicles',self.vehicle1.currentText())
        self.settings.setValue('scenario',self.scenario.currentText())
        
if __name__ == '__main__':
    app = QApplication(sys.argv)
    myapp = Openfile()
    myapp.show()
    app.exec_()