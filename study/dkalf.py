import sys
from PyQt5 import QtCore, QtGui, QtWidgets


class ClassWidget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(ClassWidget, self).__init__(parent)
        self.setGeometry(QtCore.QRect(200, 100, 670, 360))

        self.A = ClassA()
        self.B = ClassB()
        self.C = ClassC()

        grid = QtWidgets.QGridLayout(self)
        grid.addWidget(self.A, 0, 0)
        grid.addWidget(self.B, 0, 1, 1, 2)
        grid.addWidget(self.C, 1, 0, 1, 2)

class ClassA(QtWidgets.QGroupBox):
    def __init__(self, parent=None):
        super(ClassA, self).__init__(parent)
        self.setFont(QtGui.QFont("Helvetica", 10, QtGui.QFont.Normal, italic=False))      

        self.c_lay = QtWidgets.QHBoxLayout()
        fctd = "One\n\nTwo\n\nThree"
        con_strength = QtWidgets.QLabel(fctd)
        self.value = QtWidgets.QLineEdit('Test')
        self.c_lay.addWidget(con_strength)
        self.c_lay.addWidget(self.value, alignment=QtCore.Qt.AlignRight)


        self.combo = QtWidgets.QComboBox()
        self.combo.addItems(["10","12","14","16"])

        self.hbox = QtWidgets.QHBoxLayout()
        self.con = QtWidgets.QLabel("Number: ")
        self.hbox.addWidget(self.con)
        self.hbox.addWidget(self.combo)

        self.vlay = QtWidgets.QVBoxLayout()
        self.vlay.addLayout(self.hbox)
        self.vlay.addLayout(self.c_lay)
        self.vlay.addStretch()

        self.setTitle("&GroupA")
        self.setLayout(self.vlay)

        self.comth = ["10","12","14","16"]
        self.combo.activated.connect(self.setdatastrength)

    @QtCore.pyqtSlot(int)
    def setdatastrength(self, index):
        value = self.comth[index]
        self.display_data(value)


    def display_data(self, value):
        try:
            f = value
            f_value = "{}"
            self.value.setText(f_value.format(f))

        except ValueError:
            print("Error")


class ClassB(QtWidgets.QGroupBox):
    def __init__(self, parent=None):
        super(ClassB, self).__init__(parent)
        self.setFont(QtGui.QFont("Helvetica", 10, QtGui.QFont.Normal, italic=False))


        self.combo_exclass = QtWidgets.QComboBox()
        self.combo_exclass.addItems([" Very dry area"," Dry or permanently wet"," Wet, rarely dry"," Moderate humidity"," Tidal splash & spray zones"])


        self.combo_lclass = QtWidgets.QComboBox()
        self.combo_lclass.addItems(["L2","L4","L6","L8"])

        self.combo_vct = QtWidgets.QComboBox()


        self.combo_vct.addItems(["0.10","0.20","0.30","0.40",
                                        "0.50","0.60","0.70"])

        self.combo_in = QtWidgets.QComboBox()
        self.combo_in.addItems(["Class1","Class2","Class3"])        

        self.tbox = QtWidgets.QHBoxLayout()
        self.exclass = QtWidgets.QLabel("Class1: ")
        self.tbox.addWidget(self.exclass)
        self.tbox.addWidget(self.combo_exclass)


        self.mtbox = QtWidgets.QHBoxLayout()
        self.lclass = QtWidgets.QLabel("Class2: ")

        self.mtbox.addWidget(self.lclass)
        self.mtbox.addWidget(self.combo_lclass)


        self.mbbox = QtWidgets.QHBoxLayout()
        self.vct = QtWidgets.QLabel("Class3: ")
        self.mbbox.addWidget(self.vct)
        self.mbbox.addWidget(self.combo_vct)

        self.bbox = QtWidgets.QHBoxLayout()
        self.inl = QtWidgets.QLabel("Class4: ")
        self.bbox.addWidget(self.inl)
        self.bbox.addWidget(self.combo_in)


        self.grid = QtWidgets.QGridLayout()
        self.grid.addLayout(self.tbox, 0, 0, 1, 2)
        self.grid.addLayout(self.mtbox, 1, 0)
        self.grid.addLayout(self.mbbox, 2, 0)
        self.grid.addLayout(self.bbox, 3, 0)

        self.setTitle("&Group2")
        self.setLayout(self.grid)


class ClassC(QtWidgets.QGroupBox):
    def __init__(self, parent=None):
        super(ClassC, self).__init__(parent)
        self.setFont(QtGui.QFont("Helvetica", 10, QtGui.QFont.Normal, italic=False))      


        self.topone = QtWidgets.QComboBox()
        self.topone.addItems(["One","Two","Three","four"])
        self.longitudinalone = QtWidgets.QComboBox()
        self.longitudinalone.addItems(["One","Two","Three","four"])
        self.bottomone = QtWidgets.QComboBox()
        self.bottomone.addItems(["One","Two","Three","four"])
        self.stirrupone = QtWidgets.QComboBox()
        self.stirrupone.addItems(["One","Two","Three","four"])

        self.toprebar = QtWidgets.QComboBox()
        self.toprebar.addItems(["1","2","3","4","5","6","7","8","9"])
        self.longitudinalrebar = QtWidgets.QComboBox()
        self.longitudinalrebar.addItems(["1","2","3","4","5","6",
                                                   "7","8","9"])
        self.bottomrebar = QtWidgets.QComboBox()
        self.bottomrebar.addItems(["1","2","3","4","5","6","7","8","9"])
        self.stirruprebar = QtWidgets.QComboBox()
        self.stirruprebar.addItems(["1","2","3","4","5","6","7","8","9"])

        self.rebarbox = QtWidgets.QVBoxLayout()
        self.topvoid = QtWidgets.QLabel(" ")
        self.top = QtWidgets.QLabel("One: ")
        self.longitudinal = QtWidgets.QLabel("Two: ")
        self.bottom = QtWidgets.QLabel("Three: ")
        self.stirrup = QtWidgets.QLabel("Four: ") 
        self.rebarbox.addWidget(self.topvoid)
        self.rebarbox.addWidget(self.top)
        self.rebarbox.addWidget(self.longitudinal)
        self.rebarbox.addWidget(self.bottom)
        self.rebarbox.addWidget(self.stirrup)

        self.typebox = QtWidgets.QVBoxLayout()
        self.type = QtWidgets.QLabel("Type   ")  
        self.typebox.addWidget(self.type, alignment=QtCore.Qt.AlignCenter)   
        self.typebox.addWidget(self.topone)
        self.typebox.addWidget(self.longitudinalone)   
        self.typebox.addWidget(self.bottomone)    
        self.typebox.addWidget(self.stirrupone)

        self.Reinforcebox = QtWidgets.QVBoxLayout()
        self.Reinforcement = QtWidgets.QLabel("One, One")  
        self.Reinforcebox.addWidget(self.Reinforcement)   
        self.Reinforcebox.addWidget(self.toprebar)
        self.Reinforcebox.addWidget(self.longitudinalrebar)   
        self.Reinforcebox.addWidget(self.bottomrebar)    
        self.Reinforcebox.addWidget(self.stirruprebar)

        self.designstrengthbox = QtWidgets.QVBoxLayout()
        self.designsteelstrength = QtWidgets.QLabel("Four") 
        self.topsteelstrength = QtWidgets.QLabel() 
        self.longsteelstrength = QtWidgets.QLabel() 
        self.bottompsteelstrength = QtWidgets.QLabel() 
        self.stirrupsteelstrength = QtWidgets.QLabel() 
        self.designstrengthbox.addWidget(self.designsteelstrength)   
        self.designstrengthbox.addWidget(self.topsteelstrength, alignment=QtCore.Qt.AlignCenter)
        self.designstrengthbox.addWidget(self.longsteelstrength, alignment=QtCore.Qt.AlignCenter)   
        self.designstrengthbox.addWidget(self.bottompsteelstrength, alignment=QtCore.Qt.AlignCenter)    
        self.designstrengthbox.addWidget(self.stirrupsteelstrength, alignment=QtCore.Qt.AlignCenter)

        self.sbox = QtWidgets.QVBoxLayout()
        self.anytext = QtWidgets.QLabel("Any text")
        self.value = QtWidgets.QLabel("Any")
        self.value1 = QtWidgets.QLabel("Any")
        self.value2 = QtWidgets.QLabel("Any")
        self.value3 = QtWidgets.QLabel("Any")
        self.sbox.addWidget(self.anytext)
        self.sbox.addWidget(self.value)
        self.sbox.addWidget(self.value1)
        self.sbox.addWidget(self.value2)
        self.sbox.addWidget(self.value3)

        self.hlay = QtWidgets.QHBoxLayout()
        self.hlay.addStretch()
        self.hlay.addLayout(self.rebarbox)
        self.hlay.addLayout(self.typebox)
        self.hlay.addLayout(self.Reinforcebox)
        self.hlay.addLayout(self.designstrengthbox)
        self.hlay.addLayout(self.sbox)
        self.hlay.addStretch()

        self.setTitle("&GroupC")
        self.setLayout(self.hlay)
        self.rebarstrength = ["1","2","3","4"]
        self.topone.activated.connect(self.setdatatopstrength)


    @QtCore.pyqtSlot(int)
    def setdatatopstrength(self, index):
        value = self.rebarstrength[index]
        self.display_topsteeldata(value)

    @QtCore.pyqtSlot(int)    
    def display_topsteeldata(self, value):
        try:
            gammas = 1.15
            fyd = int(float(value)/gammas)
            fmt = "{}"
            self.topsteelstrength.setText(fmt.format(str(fyd)))
        except ValueError:
            print("Error")


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    w = ClassWidget()
    w.show()
    sys.exit(app.exec_())