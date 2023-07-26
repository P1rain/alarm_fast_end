import sys

from PyQt5.QtWidgets import QWidget, QApplication
from PyQt5.uic import loadUi


class AlarmChatBot(QWidget):
    def __init__(self):
        super().__init__()
        loadUi('./ui_file/AR_botchat_item.ui', self)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    myWindow = AlarmChatBot()
    myWindow.show()
    app.exec_()