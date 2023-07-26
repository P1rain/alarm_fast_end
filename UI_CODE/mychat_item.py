import sys

from PyQt5.QtWidgets import QWidget, QApplication
from PyQt5.uic import loadUi


class AlarmMychat(QWidget):
    def __init__(self, msg, send_time, parent=None):
        super().__init__(parent)
        loadUi('../ui_file/AR_mychat_item.ui', self)
        self.label_3.setText(msg)
        self.label_4.setText(send_time)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    myWindow = AlarmMychat()
    myWindow.show()
    app.exec_()