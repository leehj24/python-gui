from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5 import *
import json
import sys

class Openfile1(QWidget):
   
    def __init__(self):
        super().__init__()

        self.initUI()
       
    def initUI(self):
        # Create a QComboBox widget to select the grade
        self.grade=QComboBox()

        # Read data from the 'school.json' file
        file_path = "./config/school.json"
        with open(file_path) as file:
            data = json.load(file)
            self.json_test = data['school']

        # Populate the grade combo box with the 'grade' values from the JSON data
        for k in self.json_test:
            self.O_Name= k['grade']
            self.grade.addItem(self.O_Name)

        # 사용법 : https://learndataanalysis.org/how-to-save-your-application-settings-with-qsettings-class/
        settings = QSettings('MyQtApp','myorg')
        self.grade.setCurrentText(settings.value('grade'))

        # Connect the activated signal of the grade combo box to the 'fileopenActivated' slot
        self.grade.activated[str].connect(self.fileopenActivated)

        # Create other combo boxes for class and name selection
        self.class1=QComboBox()
        self.name=QComboBox()

        # Create a QHBoxLayout and add labels and combo boxes to it
        Hbox1 = QHBoxLayout()
        Hbox1.addWidget(QLabel('학년'))   # Label for grade
        Hbox1.addWidget(self.grade)
       
        Hbox1.addWidget(QLabel('학반'))   # Label for class
        Hbox1.addWidget(self.class1)
        self.class1.setCurrentText(settings.value('class1'))
        self.class1.activated[str].connect(self.fileopenActivated1)
       
        Hbox1.addWidget(QLabel('이름'))  # Label for name
        Hbox1.addWidget(self.name)
        self.name.setFixedSize(300,25)

        # Set the layout of the main widget to the QHBoxLayout
        self.setLayout(Hbox1)
       
    def fileopenActivated(self,text):
        self.saveSetting()

        if text == '1grade':
            # Clear the class and name combo boxes
            self.class1.clear()
            self.name.clear()

            # Add items to the class combo box based on the JSON data
            for i in self.json_test[0]['data1']: #range(0,2):
                V_name = i['class1']             #self.json_test[0]['data1'][i]['class1']
                self.class1.addItem(V_name)
        elif text == '2grade':
            self.class1.clear()
            self.name.clear()
            # Add items to the class combo box based on the JSON data for 2grade
            for i in self.json_test[1]['data1']: #range(0,2):
                V_name = i['class1']             #self.json_test[0]['data1'][i]['class1']
                self.class1.addItem(V_name)

           
        elif text == '3grade':
            self.class1.clear()
            self.name.clear()
            # Add items to the class combo box based on the JSON data for 3grade
            
            for i in self.json_test[2]['data1']: #range(0,2):
                V_name = i['class1']             #self.json_test[0]['data1'][i]['class1']
                self.class1.addItem(V_name)
        else:
            self.class1.clear()
            self.name.clear()
            
            # Clear the class and name combo boxes
        self.saveSetting()
        
    def fileopenActivated1(self,text):
        # self.saveSetting()
        
        # print(self.grade.currentText())
        print(self.class1.currentText())
        a=0
        b=0

        for k in self.json_test:
            if self.grade.currentText() == k['grade']: break
            a +=1


        for i in self.json_test[a]['data1']:
            if self.class1.currentText() == i['class1'] : break
            b +=1

        #print(self.json_test[a]['data1'][b].values())

        cnt =0
        self.name.clear()
        for m in self.json_test[a]['data1'][b].values():
            if cnt>0 :
                self.name.addItem(m)
            cnt += 1
        self.saveSetting()
    def closeEvent(self, event):
        self.saveSetting()
        super(Openfile1,self).closeEvent(event)
       
    def saveSetting(self):
        settings = QSettings('MyQtApp','myorg')
        settings.setValue('grade',self.grade.currentText())
        settings.setValue('class1',self.class1.currentText())
        # settings.setValue(self.name)
       
if __name__ == '__main__':
    app = QApplication(sys.argv)
    myapp = Openfile1()
    myapp.show()
    app.exec_()
