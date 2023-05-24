import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5 import *

class Grip(QLabel):
    def __init__(self, parent, move_widget):
        super(Grip, self).__init__(parent)
        self.move_widget = move_widget
        self.setText("+")
        self.min_height = 50

        self.mouse_start = None
        self.height_start = self.move_widget.height()
        self.resizing = False
        self.setMouseTracking(True)
        
    def showEvent(self, event):
        super(Grip, self).showEvent(event)
        self.reposition()

    def mousePressEvent(self, event):
        super(Grip, self).mousePressEvent(event)
        self.resizing = True
        self.height_start = self.move_widget.height()
        self.mouse_start = event.pos()

    def mouseMoveEvent(self, event):
        super(Grip, self).mouseMoveEvent(event)
        if self.resizing:
            delta = event.pos() - self.mouse_start
            height = self.height_start + delta.y()
            if height > self.min_height:
                self.move_widget.setFixedHeight(height)
            else:
                self.move_widget.setFixedHeight(self.min_height)

        #self.reposition()                                       # <-  ---

    def mouseReleaseEvent(self, event):
        super(Grip, self).mouseReleaseEvent(event)
        self.resizing = False

        self.reposition()           

    def reposition(self):
        rect = self.move_widget.geometry()
        self.move(rect.right(), rect.bottom())


class Dialog(QDialog):
    def __init__(self):
        super(Dialog, self).__init__()
        layout = QVBoxLayout()
        self.setLayout(layout)
        list_widget = QListWidget()
        layout.addWidget(list_widget)
        gripper = Grip(self, list_widget)

        layout.addWidget(QLabel("Test"))

        self.setGeometry(200, 500, 200, 500)
        
if __name__ == '__main__':
    app = QApplication(sys.argv)
    myapp = Dialog()
    myapp.show()
    app.exec_()