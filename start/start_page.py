import sys

from PyQt5.QtWidgets import QWidget, QApplication
from PyQt5.uic import loadUi

from UI_CODE.login_page import AlarmLogin
from CODE.class_client import ClientApp


class AlarmStart(QWidget):
    def __init__(self, client_app=ClientApp):
        isinstance(client_app, ClientApp)
        super().__init__()
        loadUi('./ui_file/AR_start_page.ui', self)
        self.client_app = client_app
        self.window_option()
        self.btn_event()

    def window_option(self):
        """프로그램 실행 옵션"""
        self.stackedWidget.setCurrentIndex(0)

    def btn_event(self):
        """버튼 클릭 이벤트 함수"""
        self.next_btn.clicked.connect(lambda x: self.stackedWidget.setCurrentIndex(1))
        self.next_btn_2.clicked.connect(self.go_login_page)
        self.back_btn.clicked.connect(lambda x: self.stackedWidget.setCurrentIndex(0))

    def go_login_page(self):
        """로그인 UI로 이동 함수"""
        login = AlarmLogin(self.client_app)
        login.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    client_app = ClientApp()
    myWindow = AlarmStart(client_app)
    myWindow.show()
    app.exec_()