import pandas as pd

class ReadFile:
    def data(self):
        self.file = pd.read_excel('./scenario_1.xlsx', sheet_name = None)
        self.number = self.file.keys() # 시트 이름 
        self.sheetnb = list(self.number)
        
class TestManager:
    File = ReadFile(); File.data()
    def signal1(self):
        sheet1 = self.File.file[self.File.sheetnb[0]]
        self.Allist1 = []
        for i in range(len(sheet1.columns)):
            target = sheet1.iloc[:,i] # 열 추출
            self.Allist1.append(target)
        # print(self.Allist1[1])
        
class TestManager1:
    File = ReadFile(); File.data()
    def signal2(self):
        sheet2 = self.File.file[self.File.sheetnb[1]]
        # sheet2 = self.File.file['CLU_01_20ms']
        self.Allist2 = []
        for i in range(len(sheet2.columns)):
            target = sheet2.iloc[:,i] # 열 추출
            self.Allist2.append(target)
        # print(self.Allist2[2][3]) #self.Allist2[열][행]
        
class TestManager2:
    File = ReadFile(); File.data()
    def signal3(self):
        sheet3 = self.File.file[self.File.sheetnb[2]]
        self.Allist3 = []
        for i in range(len(sheet3.columns)):
            target = sheet3.iloc[:,i] # 열 추출
            self.Allist3.append(target)
        # print(self.Allist3[1])  #[행][열]
        
class List:
    def name(self):
        data1 = TestManager(); data1.signal1()
        data2 = TestManager1(); data2.signal2()
        data3 = TestManager2(); data3.signal3()
        # List = [data1.Allist1[1]]
        self.List = [data1.Allist1,data2.Allist2,data3.Allist3]
        # print(self.List[0][1]) #행한개짜리 시트임 
        # print(self.List[1][1])
        
if __name__ == '__main__':
    List().name()

