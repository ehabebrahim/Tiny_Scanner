from test import *
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtGui import *
from PyQt5.uic import loadUi
import sys

class UI_MainWindow(QMainWindow):
    def __init__(self):
        super(UI_MainWindow, self).__init__()
        loadUi("/media/ehab/Data 2/faculty of engineering ain shams/4th CSE/System Software/project/Scanner.ui", self)
        pixmap = QPixmap("/media/ehab/Data 2/faculty of engineering ain shams/4th CSE/System Software/project/new.png")
        self.label.setPixmap(pixmap)
        self.label.resize(pixmap.width(), pixmap.height())
        self.pushButton.clicked.connect(self.scan)
        self.textEdit.setTextColor(QColor(255, 0, 0))
        self.textEdit_2.setTextColor(QColor(255, 0, 0))

    def scan(self):
        #print(self.textEdit.toPlainText())
        out = get_token(self.textEdit.toPlainText())
        for i in out:
            self.textEdit_2.append(i)




app = QApplication(sys.argv)
widget = QtWidgets.QStackedWidget()
widget.addWidget(UI_MainWindow())
widget.setFixedWidth(1050)
widget.setFixedHeight(1000)
widget.show()
app.exec_()

