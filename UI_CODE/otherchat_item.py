import sys

from PyQt5.QtWidgets import QWidget, QApplication
from PyQt5.uic import loadUi


class AlarmOtherchat(QWidget):
    def __init__(self, msg, send_time, other_nickname, parent=None):
        super().__init__(parent)
        loadUi('../ui_file/AR_userchat_item.ui', self)
        self.label_3.setText(msg)
        self.label_4.setText(send_time)
        self.label_2.setText(other_nickname)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    myWindow = AlarmOtherchat()
    myWindow.show()
    app.exec_()