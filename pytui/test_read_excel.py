import sys
from PyQt5.QtWidgets import *
import pandas as pd
# 시나리오[시그널[타겟리스트[1,2,3...]]
# 시트/타임/시그널 class

class sheets:
    def __init__(self, a, b, c):
        self.a = a
        self.b = b
        self.c = c
        
class file:
    def __init__(self, file1, file2, file3):
        self.file1 = file1
        self.file2 = file2
        self.file3 = file3

class writefile:
    a = 'CLU_01_20ms'
    b = 'CLU_02_100ms'
    c = 'WHL_01_10ms'
    
    file1 =  pd.read_excel('./scenario_1.xlsx', sheet_name = a)
    file2 =  pd.read_excel('./scenario_1.xlsx', sheet_name = b)
    file3 =  pd.read_excel('./scenario_1.xlsx', sheet_name = c)

    def readfile(self):
        
        sheet_name = [self.a,self.b,self.c] #시트 이름 
        self.name1 = [] ; self.name2 = [] ; self.name3 = [] 
        
        for i in range(len(self.file1.columns)):
            Signalist1 = self.file1.columns[i] #1시트 첫번째 헹
            self.name1.append(Signalist1)
            
        for i in range(len(self.file2.columns)):
            Signalist2 = self.file2.columns[i] #2시트 첫번째 행
            self.name2.append(Signalist2)
            
        for i in range(len(self.file3.columns)):
            Signalist3 = self.file3.columns[i] #3시트 첫번째 행
            self.name3.append(Signalist3)
            
        SList = [self.name1, self.name2, self.name3] # all signal name list
    
        time1 = self.file1[self.name1[0]]
        time2 = self.file2[self.name2[0]]
        time3 = self.file3[self.name3[0]]
        timelist = [time1,time2,time3] 
        
        # print(SList[0][2],self.name1[2])   

class  writeSignal:
    
    def signal(self):
        File = writefile() ; File.readfile()
        Sign1 =[] ; Sign2 =[] ; Sign3 =[] 
        
        for i in range(1,len(File.name1)):
            signal1 = File.file1[File.name1[i]] # 1시트 특정 열 전체
            Sign1.append(signal1)
            
        for i in range(1,len(File.name2)):
            signal2 = File.file2[File.name2[i]] # 2시트 특정 열 전체
            Sign2.append(signal2)
            
        for i in range(1,len(File.name3)):
            signal3 =File.file3[File.name3[i]] # 3시트 특정 열 전체
            Sign3.append(signal3)
        
        print(Sign1[1])
        
if __name__ == '__main__':
    # print(writefile())
    # writefile().readfile()
    writeSignal().signal()

