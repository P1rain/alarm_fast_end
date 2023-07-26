import sys

from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QWidget, QApplication
from PyQt5.uic import loadUi
import datetime

from UI_CODE.mychat_item import AlarmMychat


class AlarmMain(QWidget):
    chatting_signal = pyqtSignal(str)

    def __init__(self, clientapp):
        super().__init__()
        loadUi('../ui_file/AR_main_page.ui', self)
        self.clientapp = clientapp
        self.clientapp.set_widget(self)
        self.nickname = self.clientapp.user_nickname
        self.window_option()
        self.btn_event()
        self.signal_event()
        self.now_time()

    def window_option(self):
        """프로그램 실행 옵션"""
        self.stackedWidget.setCurrentIndex(0)
        self.chatbot_btn.setChecked(True)

    def now_time(self):
        """실시간 시간 출력 기능 함수"""
        send_time = datetime.datetime.today().strftime("%p %I:%M")
        if send_time[:2] == "PM":
            send_time = datetime.datetime.today().strftime("오후 " + "%I:%M")
        elif send_time[:2] == "AM":
            send_time = datetime.datetime.today().strftime("오전 " + "%I:%M")
        return send_time

    def signal_event(self):
        """시그널 이벤트 함수"""
        pass

    def btn_event(self):
        """버튼 클릭 이벤트 함수"""
        self.chatbot_btn.clicked.connect(self.go_chat_bot)
        self.userchat_btn.clicked.connect(self.go_user_chat)
        self.music_btn.clicked.connect(self.go_music_option)
        self.myinfo_btn.clicked.connect(self.go_myinfo)
        self.send_chatbot_btn.clicked.connect(self.msg_send_function)
        self.all_send_btn.clicked.connect(self.msg_send_all)

    def msg_send_function(self):
        """챗봇에게 전송 버튼 클릭 이벤트 함수"""
        msg = self.chat_edit.toPlainText()
        send_time_ = self.now_time()
        self.chat_edit.clear()
        self.clientapp.send_msg_chatbot(msg, send_time_)
        self.chatbot_addwidget(msg, send_time_)

    def chatbot_addwidget(self, msg, send_time_):
        """채팅봇 대화방에서 텍스트 addwidget 이벤트 함수"""
        my_msg = msg
        now_time = send_time_
        mychat_item = AlarmMychat(my_msg, now_time)
        mychat_item.setParent(self.scrollAreaWidgetContents)
        self.scrollArea.widget().layout().insertWidget(len(self.scrollArea.widget().layout())-1, mychat_item)

    def msg_send_all(self):
        """전체채팅 기능 함수"""
        msg = self.chat_edit_3.toPlainText()
        send_time_ = self.now_time()
        self.chat_edit_3.clear()
        self.clientapp.send_msg_all(msg, send_time_)


    def go_chat_bot(self):
        """챗봇과의 채팅 페이지 이동 함수"""
        self.stackedWidget.setCurrentIndex(0)

    def go_user_chat(self):
        """유저와의 채팅 페이지 이동 함수"""
        self.stackedWidget.setCurrentIndex(1)

    def go_music_option(self):
        """알람음 설정 페이지 이동 함수"""
        self.stackedWidget.setCurrentIndex(2)

    def go_myinfo(self):
        """나의 정보 페이지 이동 함수"""
        self.stackedWidget.setCurrentIndex(3)
        self.nickname_lbl.setText(self.nickname)


# if __name__ == '__main__':
#     app = QApplication(sys.argv)
#     myWindow = AlarmMain()
#     myWindow.show()
#     app.exec_()