import sys
import time

from PyQt5.QtCore import QTimer, pyqtSignal
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QWidget, QApplication
from PyQt5.uic import loadUi

from UI_CODE.main_page import AlarmMain


class AlarmLogin(QWidget):
    join_access_signal = pyqtSignal(str)
    log_in_signal = pyqtSignal(bool)

    def __init__(self, clientapp):
        super().__init__()
        loadUi('../ui_file/AR_login_page.ui', self)
        self.clientapp = clientapp
        self.clientapp.set_widget(self)
        self.window_option()
        self.btn_event()
        self.lbl_event()
        self.qtimer_event()
        self.signal_event()

    def signal_event(self):
        """시그널 이벤트 함수"""
        self.log_in_signal.connect(self.log_in_res)
        self.join_access_signal.connect(self.join_access_res)

    def window_option(self):
        """프로그램 실행 옵션"""
        self.stackedWidget.setCurrentIndex(0)
        self.error_lbl.setText("")
        self.error_lbl_2.setText("")
        self.ar_list = ['../UI_img/알람시계.png', '../UI_img/알람시계(좌).png', '../UI_img/알람시계.png', '../UI_img/알람시계(우).png']
        self.ar_list2 = ['../UI_img/늦잠3.png', '../UI_img/캡처.png']

    def qtimer_event(self):
        """qtimer 실행 함수"""
        qtimer = QTimer(self)
        qtimer.start(1)
        qtimer.timeout.connect(self.go_timer_event)
        qtimer2 = QTimer(self)
        qtimer2.start(1000)
        qtimer2.timeout.connect(self.go_timer_event2)
        self.cnt = 1
        self.cnt2 = 0

    def go_timer_event(self):
        """알람시계 이미지 움짤 이벤트 함수"""
        ar_list_ = [self.ar_list]
        self.ar_lbl.setPixmap(QPixmap(ar_list_[0][self.cnt]))
        self.cnt += 1
        if self.cnt == 4:
            self.cnt = 1

    def go_timer_event2(self):
        """늦잠 이미지 움짤 이벤트 함수"""
        ar_list = [self.ar_list2]
        self.ani_lbl.setPixmap(QPixmap(ar_list[0][self.cnt2]))
        self.cnt2 += 1
        if self.cnt2 == 2:
            self.cnt2 = 0

    def btn_event(self):
        """버튼 클릭 이벤트 함수"""
        self.login_btn.clicked.connect(self.login_check)
        self.back_btn.clicked.connect(self.go_home_page)
        self.join_btn.clicked.connect(self.join_access)

    def lbl_event(self):
        """라벨 클릭 이벤트 함수"""
        self.join_lbl.mousePressEvent = self.go_join_page  # 회원가입 스택위젯 이동

    def go_home_page(self):
        """회원가입 페이지에서 뒤로가기 클릭시 로그인 페이지로 이동 함수(작성하던 lineEdit clear)"""
        self.id_line.clear()
        self.pw_line.clear()
        self.pw_checkline.clear()
        self.name_line.clear()
        self.stackedWidget.setCurrentIndex(0)

    def login_check(self):
        """로그인 체크 함수"""
        id_login = self.lineEdit.text()
        pw_login = self.lineEdit_2.text()
        if len(id_login) == 0:
            self.error_lbl.setText("아이디를 입력해주세요")
            return
        elif len(pw_login) == 0:
            self.error_lbl.setText("비밀번호를 입력해주세요")
            return

        self.log_in(id_login, pw_login)

    def log_in(self, id_login, pw_login):
        """로그인 정보 client로 넘겨주는 함수"""
        self.clientapp.send_id_and_pw_login_access(id_login, pw_login)

    def log_in_res(self, return_result):
        """ui 로그인 시도 결과"""
        if return_result:
            self.go_main_page()
        else:
            self.error_lbl.setText("아이디 또는 비밀번호가 일치하지 않습니다.")

    def go_join_page(self, e):
        """회원가입 페이지로 이동하는 함수"""
        self.stackedWidget.setCurrentIndex(1)

    def join_access(self):
        """회원가입 승인 함수"""
        join_id = self.id_line.text()
        join_pw = self.pw_line.text()
        join_pw_check = self.pw_checkline.text()
        join_nickname = self.name_line.text()
        if len(join_id) == 0:
            self.error_lbl_2.setText("아이디를 입력해주세요.")
            return
        elif len(join_pw) == 0:
            self.error_lbl_2.setText("비밀번호를 입력해주세요.")
            return
        elif len(join_pw_check) == 0:
            self.error_lbl_2.setText("비밀번호를 입력해주세요.")
            return
        elif len(join_nickname) == 0:
            self.error_lbl_2.setText("닉네임을 입력해주세요.")
            return

        self.clientapp.send_join_access(join_id, join_pw, join_nickname)

    def join_access_res(self, return_result):
        """회원가입 결과 함수"""
        pw_check = self.pw_line.text()
        pw_recheck = self.pw_checkline.text()
        if return_result == "00":
            self.error_lbl_2.setText("아이디와 닉네임이 이미 존재합니다.")
            return
        elif pw_check != pw_recheck:
            self.error_lbl_2.setText("비밀번호가 일치하지 않습니다.")
            return
        elif return_result == "10":
            self.error_lbl_2.setText("아이디가 이미 존재합니다.")
            return
        elif return_result == "01":
            self.error_lbl_2.setText("닉네임이 이미 존재합니다.")
            return
        elif return_result == "11":
            self.id_line.clear()
            self.pw_line.clear()
            self.pw_checkline.clear()
            self.name_line.clear()
            self.stackedWidget.setCurrentIndex(0)

    def go_main_page(self):
        """메인페이지 UI로 이동 함수"""
        self.main_ = AlarmMain(self.clientapp)
        self.close()
        self.main_.show()


# if __name__ == '__main__':
#     app = QApplication(sys.argv)
#     myWindow = AlarmLogin()
#     myWindow.show()
#     app.exec_()