import sys
from PyQt5.QtWidgets import *
import pandas as pd

class DataRead(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.read()
    
    def initUI(self):
        
        self.texta = QTextBrowser(self)
        self.textb = QTextBrowser(self)
        self.textc = QTextBrowser(self)
        self.textd = QTextBrowser(self)
        self.texte = QTextBrowser(self)
        
        self.vbox = QVBoxLayout()
        self.vbox.addWidget(self.texta)
        self.vbox.addWidget(self.textb)
        self.vbox.addWidget(self.textc)
        self.vbox.addWidget(self.textd)
        self.vbox.addWidget(self.texte)
        self.setLayout(self.vbox)
        
        self.setGeometry(100, 150, 950, 800)
        self.show()
        
    def read(self):
        
        a = 'CLU_01_20ms'
        b = 'CLU_02_100ms'
        c = 'WHL_01_10ms'
        
        file1 =  pd.read_excel('./scenario_1.xlsx', sheet_name = a)
        file2 =  pd.read_excel('./scenario_1.xlsx', sheet_name = b)
        file3 =  pd.read_excel('./scenario_1.xlsx', sheet_name = c)
        
        sheet_name = [a,b,c]
        name = [file1, file2, file3]
        
        Signalist = file1.columns
        # print(file1['time'])
        # time1 = file1[Signalist[0]]
        
        time1 = file1[Signalist[0]]
        time2 = file2[Signalist[1]]
        time3 = file3[Signalist[2]]
        timelist = [time1,time2,time3]
        
        signal1 = file1[Signalist[1]]
        signal2 = file1[Signalist[2]]
        signal3 = file1[Signalist[3]]
        signal4 = file1[Signalist[4]]
        signal5 = file1[Signalist[5]]
        
        # signal1 = file1['CLU_Crc1Val']
        # signal2 = file1['CLU_AlvCnt1Val']
        # signal3 = file1['CLU_SpdUnitTyp']
        # signal4 = file1['CLU_DisSpdDcmlVal']
        # signal5 = file1['CLU_DisSpdVal']
        
        signalist = [signal1, signal2, signal3, signal3, signal4, signal5]
        
        self.texta.append(str(name))
        self.textb.append(str(timelist))
        self.textc.append(str(signal1)) #특정 열 전체
        self.textd.append(str(signalist))
        # self.textd.append(str(sheet_name)) #시트이름
        self.texte.append(str(Signalist[1])) # 시그널이름
        
        # for i in range(0,3):
        #     file  = pd.read_excel('./scenario_1.xlsx', sheet_name = i)
        
if __name__ == '__main__':
    app = QApplication(sys.argv)
    myapp = DataRead()
    myapp.show()
    app.exec_()
