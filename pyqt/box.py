import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QHBoxLayout, QVBoxLayout


class MyApp(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        okButton = QPushButton('OK') 
        cancelButton = QPushButton('Cancel')

        hbox = QHBoxLayout() #수평박스
        hbox.addStretch(3) #숫자= 양쪽의 빈공간
        hbox.addWidget(okButton)
        hbox.addWidget(cancelButton)
        hbox.addStretch(3)

        vbox = QVBoxLayout()#수직박스
        vbox.addStretch(3) #위아래 빈공간
        vbox.addLayout(hbox)
        vbox.addStretch(1)

        self.setLayout(vbox)

        self.setWindowTitle('Box Layout')
        self.setGeometry(300, 300, 300, 200)
        self.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyApp()
    sys.exit(app.exec_())