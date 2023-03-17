import sys
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QTransform
from PyQt5.QtWidgets import QApplication, QLabel, QMainWindow


class MainWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.setFixedSize(640, 480)

        label = QLabel(self)
        label.move(250, 50)

        pixmap = QPixmap("car.png")
        label.setPixmap(pixmap)
        xform = QTransform()
        xform.rotate(90)
        xformed_pixmap = pixmap.transformed(xform, Qt.SmoothTransformation)
        label.setPixmap(xformed_pixmap)
        label.adjustSize()


app = QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec_()