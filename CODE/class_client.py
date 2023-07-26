import datetime
import socket
import time
from threading import *
from common.class_json import *
from DataBase.class_user import User
from DataBase.class_msg import Message


class ClientApp:
    HOST = '127.0.0.1'
    PORT = 9999
    BUFFER = 50000
    FORMAT = "utf-8"
    HEADER_LENGTH = 30

    log_in = "log_in"
    check_join_id = "check_join_id"
    check_join_nickname = "check_join_nickname"
    join_user = "join_user"
    send_chatbot = "send_chatbot"
    send_all = "send_all"

    def __init__(self):
        self.user_id = None
        self.client_socket = None
        self.config = None
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect((self.HOST, self.PORT))
        self.encoder = ObjEncoder()
        self.decoder = ObjDecoder()

        self.receive_thread = Thread(target=self.receive_message)
        self.receive_thread.daemon = True
        self.receive_thread.start()

    def set_widget(self, widget_):
        self.client_widget = widget_
    
    # 로그인
    def send_id_and_pw_login_access(self, login_id, login_pw):
        data_msg = User(None, login_id, login_pw, None)
        data_msg_str = self.encoder.toJSON_as_binary(data_msg)
        header_data = self.log_in
        self.fixed_volume(header_data, data_msg_str)
    
    # 회원가입
    def send_join_access(self, join_id, join_pw, join_nickname):
        data_msg = User(None, join_id, join_pw, join_nickname)
        data_msg_str = self.encoder.toJSON_as_binary(data_msg)
        header_data = self.join_user
        self.fixed_volume(header_data, data_msg_str)

    # 챗봇에게 보내는 메세지
    def send_msg_chatbot(self, msg, send_time):
        data_msg = Message(self.user_id, msg, send_time)
        data_msg_str = self.encoder.toJSON_as_binary(data_msg)
        header_data = self.send_chatbot
        self.fixed_volume(header_data, data_msg_str)

    # 전체채팅
    def send_msg_all(self, msg, send_time):
        data_msg = Message(self.user_id, self.user_nickname, msg, send_time)
        print(data_msg)
        data_msg_str = self.encoder.toJSON_as_binary(data_msg)
        header_data = self.send_all
        self.fixed_volume(header_data, data_msg_str)

    # 길이 맞춰서 서버로 전송시켜줌
    def fixed_volume(self, header, data):
        header_msg = f"{header:<{self.HEADER_LENGTH}}".encode(self.FORMAT)
        data_msg = f"{data:<{self.BUFFER - self.HEADER_LENGTH}}".encode(self.FORMAT)
        self.client_socket.send(header_msg + data_msg)

    # 서버에서 정보를 받음
    def receive_message(self):
        while True:
            return_result_ = self.client_socket.recv(self.BUFFER).decode(self.FORMAT)
            response_header = return_result_[:self.HEADER_LENGTH].strip()
            response_data = return_result_[self.HEADER_LENGTH:].strip()
            # 로그인 결과
            if response_header == self.log_in:
                if response_data == '.':
                    self.client_widget.log_in_signal.emit(False)
                else:
                    object_data = self.decoder.binary_to_obj(response_data)
                    self.user_id = object_data.user_id
                    self.user_nickname = object_data.user_nickname
                    self.client_widget.log_in_signal.emit(True)

            # 회원가입 정보
            if response_header == self.join_user:
                self.client_widget.join_access_signal.emit(response_data)

            # 챗봇 메세지
            if response_header == self.send_chatbot:
                self.client_widget.chatting_signal.emit(response_data)
