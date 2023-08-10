import pandas as pd

class TestManager:
    file1 =  pd.read_excel('./scenario_1.xlsx', sheet_name = None)
    number = file1.keys() ; sheetnb = list(number)
    
    def cido(self):
        for i in range(len(self.file1)):
            print(len(self.file1),i)
    def signal1(self):
        sheet1 = self.file1[self.sheetnb[0]]
        self.Allist1 = []
                
        for i in range(len(self.file1)):
            target = sheet1.iloc[:,i] # 열 추출
            self.Allist1.append(target)
        print(self.Allist1[1])
            
    def signal2(self):
        sheet2 = self.file1[self.sheetnb[1]] # 시트이름
        self.Allist2 = []
        
        for i in range(len(self.file1)):
            target = sheet2.iloc[:,i] # 열 추출
            self.Allist2.append(target)
        # print(self.Allist2)
        
    def signal3(self):
        sheet3 = self.file1[self.sheetnb[2]] # 시트이름
        self.Allist3 = []
        
        for i in range(len(self.file1)):
            target = sheet3.iloc[:,i] # 열 추출
            self.Allist3.append(target)
        # print(self.Allist3)
        
    def List(self):
        data = TestManager(); data.signal1()
        data1 = TestManager(); data1.signal2()
        data2 = TestManager(); data2.signal3()
        self.list = [data.Allist1,data1.Allist2[3],data2.Allist3[3]]
        # list = [TestManager().signal1(),TestManager().signal2(),TestManager().signal3()]
        # print(list)
        
if __name__ == '__main__':
    TestManager().List()

