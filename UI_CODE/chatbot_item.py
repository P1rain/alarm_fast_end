import sys

from PyQt5.QtWidgets import QWidget, QApplication
from PyQt5.uic import loadUi


class AlarmChatBot(QWidget):
    def __init__(self, msg, now_time, parent=None):
        super().__init__(parent)
        loadUi('../ui_file/AR_botchat_item.ui', self)
        self.label_3.setText(msg)
        self.label_4.setText(now_time)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    myWindow = AlarmChatBot()
    myWindow.show()
    app.exec_()