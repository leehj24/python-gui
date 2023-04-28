import sys
import pandas as pd
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import matplotlib.pyplot as plt


class Main(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        #불러올 파일 형식(excel or csv) 선택 창
        self.file_open_box = QComboBox(self)
        self.file_open_box.addItem('None')
        self.file_open_box.addItem('Excel File')
        self.file_open_box.addItem('CSV File')

        self.file_open_box.setToolTip('불러올 파일 형식을 선택합니다.')
    
        self.file_open_box.activated[str].connect(self.fileopenActivated)

    #그래프의 스타일 선택 창
        self.graph_theme_box = QComboBox(self)
        self.graph_theme_box.addItem('default')
        self.graph_theme_box.addItem('classic')
        self.graph_theme_box.addItem('dark_background')
        self.graph_theme_box.addItem('Solarize_Light2')
        self.graph_theme_box.addItem('ggplot')
        self.graph_theme_box.addItem('seaborn-whitegrid')

        self.graph_theme_box.setToolTip(('그래프 스타일을 선택합니다.'))
    
        self.graph_theme_box.activated[str].connect(self.onActivated)
        
        #그래프 그리기 / 지우기 버튼 정의    
        self.graph_erase_btn = QPushButton('Graph List\n     Item Erase     ')
        self.graph_erase_btn.adjustSize()
    
        self.graph_erase_btn.setToolTip('Graph List에서 선택한 항목을 지우고 그래프를 다시 그립니다.')
    
        self.graph_erase_btn.clicked.connect(self.grapherase)
        self.graph_erase_btn.clicked.connect(self.graphplot)

        #그래프 종류 결정 버튼 정의
        self.line_graph_btn = QRadioButton('Line Plot')
        self.line_graph_btn.setChecked(True)           
        self.line_graph_btn.setToolTip('선형 그래프를 그립니다.')
        self.line_graph_btn.clicked.connect(self.graph_selec)

        self.hist_graph_btn = QRadioButton('Histogram')
        self.hist_graph_btn.setToolTip('막대형 그래프를 그립니다.')
        self.hist_graph_btn.clicked.connect(self.graph_selec)
        
        self.setGeometry(300, 300, 600, 600)  # x, y, w, h
        self.setWindowTitle('QPaint Move')
        
        #파일의 컬럼을 넣을 List 생성
        self.listwidget_01 = QListWidget(self)
        self.listwidget_02 = QListWidget(self)

        self.listwidget_01.setToolTip('불러온 파일의 컬럼명을 보여줍니다.\n원하는 컬럼을 더블클릭하면 그래프로 보여줍니다.')
        self.listwidget_02.setToolTip('선택한 컬럼명을 보여줍니다.\n항목을 선택한 후 Erase 버튼을 사용하여 삭제할 수 있습니다.')

        #listwidget_01에서 선택한 항목을 listwidget_02에 보여주면서 그래프 생성
        self.listwidget_01.itemDoubleClicked.connect(self.doubleclicked_listwidget)
        self.listwidget_01.itemDoubleClicked.connect(self.graphplot)

    #각 List의 이름 생성
        self.label1 = QLabel('< Column List >')
        self.label2 = QLabel('< Graph List >')
        self.label3 = QLabel('')
        
        
    #위치 결정
        hbox_1 = QHBoxLayout()
        hbox_1.addWidget(self.file_open_box)
        hbox_1.addWidget(self.graph_theme_box)
        hbox_1.addWidget(self.graph_erase_btn)

        hbox_2 = QHBoxLayout()
        hbox_2.addWidget(self.line_graph_btn)
        hbox_2.addStretch(1)
        hbox_2.addWidget(self.hist_graph_btn)

        vbox_1 = QVBoxLayout()
        vbox_1.addLayout(hbox_1)
        vbox_1.addLayout(hbox_2)

        vbox_2 = QVBoxLayout()
        vbox_2.addWidget(self.label3)
        vbox_2.addWidget(self.label1)
        vbox_2.addWidget(self.listwidget_01)
        vbox_2.addWidget(self.label2)
        vbox_2.addWidget(self.listwidget_02)

        vbox_3 = QVBoxLayout()
        vbox_3.addLayout(vbox_1)
        vbox_3.addLayout(vbox_2)

        hbox_3 = QHBoxLayout()
        hbox_3.addStretch(1)
        hbox_3.addLayout(vbox_3)
        hbox_3.addStretch(1)

        self.setLayout(hbox_3)

        self.center()       
        self.show()

    def fileopenActivated(self, text): #파일 형식 선택 
      if text == 'Excel File':
          self.listwidget_01.clear()
          self.data = pd.DataFrame()
          fname01 = QFileDialog.getOpenFileName(self)
        
          try:
            self.data=pd.read_excel(fname01[0], index_col=0)
            i = 1      
            for i in range(len(self.data.columns)):
              temp_Item = QListWidgetItem(self.data.columns[i])
              self.listwidget_01.addItem(temp_Item)

          except ValueError:
            QMessageBox.warning(self, '형식이 일치하지 않습니다.', '형식이 일치하는 파일을 불러오시오')     

          except FileNotFoundError:
            QMessageBox.warning(self, '파일이 없습니다.', '형식에 맞는 파일을 선택하시오')

      if text == 'CSV File':
          self.listwidget_01.clear()
          self.data = []
          fname02 = QFileDialog.getOpenFileName(self)         

          try:
            self.data=pd.read_csv(fname02[0], index_col=0)
            i = 1      
            for i in range(len(self.data.columns)):
              temp_Item = QListWidgetItem(self.data.columns[i])
              self.listwidget_01.addItem(temp_Item)

          except UnicodeDecodeError:
            QMessageBox.warning(self, '형식이 일치하지 않습니다', '형식이 일치하는 파일을 불러오시오')      

          except FileNotFoundError:
            QMessageBox.warning(self, '파일이 없습니다.', '형식에 맞는 파일을 선택하시오')
            
    def onActivated(self, value): #그래프 스타일 결정
        plt.style.use(value)
        self.graphplot()
        
    def doubleclicked_listwidget(self): #그리고자 하는 column을 선택
        list_item = self.listwidget_01.selectedItems()

        for item in list_item:
            self.listwidget_02.addItem(item.text())
            
            
    def graph_selec(self): #선형/막대형 그래프 선택
      if self.line_graph_btn.isChecked():
          self.graphplot()

      if self.hist_graph_btn.isChecked():
          self.graphplot()
          
    def graphplot(self):#그래프 그리기
        num = 0
        num = self.listwidget_02.count()      
        sel_culm = []                         
        new_data = pd.DataFrame()            
        selection = []

        if num == 0:
            plt.close()

        for i in range(0,num):
            selection = self.listwidget_02.item(i)
            sel_culm = selection.text()          
            if sel_culm in self.data.columns:
                new_data[sel_culm] = self.data[sel_culm]

            if self.line_graph_btn.isChecked():
                plt.close()
                plt.plot(new_data, label=new_data.columns)
                plt.xticks(rotation=90)
                plt.margins(x=0,y=0)
                legend = plt.legend()    
                legend.set_draggable(True) 
                plt.grid(True)
                plt.show()      

            if self.hist_graph_btn.isChecked():
                plt.close()
                plt.hist(new_data, label=new_data.columns)
                plt.xticks(rotation=90)
                plt.margins(x=0,y=0)
                legend = plt.legend()     
                legend.set_draggable(True)    
                plt.grid(True)
                plt.show()      
   
    def grapherase(self): #Column 지우기
        erase_item = self.listwidget_02.currentRow()
        self.listwidget_02.takeItem(erase_item)
        self.graphplot()
        
    def center(self): # 중심배치   
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())
      
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Main()
    sys.exit(app.exec_())