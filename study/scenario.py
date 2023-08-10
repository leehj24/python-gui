import sys
from PyQt5.QtWidgets import *
import pandas as pd
# 시트/타임/시그널 class
class DataRead(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.cido()
        # self.read()
        
    def initUI(self):
        self.read()
        
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
        self.sheet_name = [a,b,c] #시트 이름 
        
        self.file1 =  pd.read_excel('./scenario_1.xlsx', sheet_name = a)
        self.file2 =  pd.read_excel('./scenario_1.xlsx', sheet_name = b)
        self.file3 =  pd.read_excel('./scenario_1.xlsx', sheet_name = c)
        
        self.sido1 = [] ; self.sido2 = [] ; self.sido3 = [] 
        
        for i in range(len(self.file1.columns)):
            self.Signalist1 = self.file1.columns[i] #1시트 첫번째 열
            self.sido1.append(self.Signalist1)
            
        for i in range(len(self.file2.columns)):
            self.Signalist2 = self.file2.columns[i] #2시트 첫번째 열
            self.sido2.append(self.Signalist2)
            
        for i in range(len(self.file3.columns)):
            self.Signalist3 = self.file3.columns[i] #3시트 첫번째 열
            self.sido3.append(self.Signalist3)
            
        self.SList = [self.sido1, self.sido2, self.sido3] # all signal name list
    
        self.time1 = self.file1[self.sido1[0]]
        self.time2 = self.file2[self.sido2[0]]
        self.time3 = self.file3[self.sido3[0]]
        self.timelist = [self.time1,self.time2,self.time3] 
        
        self.Sign1 =[] ; self.Sign2 =[] ; self.Sign3 =[] 
        
        for i in range(1,len(self.sido1)):
            self.signal1 = self.file1[self.sido1[i]] # 1시트 특정 열 전체
            self.Sign1.append(self.signal1)
            
        for i in range(1,len(self.sido2)):
            self.signal2 = self.file2[self.sido2[i]] # 2시트 특정 열 전체
            self.Sign2.append(self.signal2)
            
        for i in range(1,len(self.sido3)):
            self.signal3 = self.file3[self.sido3[i]] # 3시트 특정 열 전체
            self.Sign3.append(self.signal3)
        
        
    def cido(self):
        # self.texta.append(str(self.SList))
        self.textb.append(str(self.timelist))
        self.textc.append(str(self.Sign2[0])) 
        self.textd.append(str(self.SList))
        # self.texte.append(str(self.sheet_name)) #시트이름
        
if __name__ == '__main__':
    app = QApplication(sys.argv)
    myapp = DataRead()
    myapp.show()
    app.exec_()
