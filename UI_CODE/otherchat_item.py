import sys

from PyQt5.QtWidgets import QWidget, QApplication
from PyQt5.uic import loadUi


class AlarmOtherchat(QWidget):
    def __init__(self):
        super().__init__()
        loadUi('../ui_file/AR_userchat_item.ui', self)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    myWindow = AlarmOtherchat()
    myWindow.show()
    app.exec_()