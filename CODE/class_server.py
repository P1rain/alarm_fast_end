import os
import threading
from socket import *
from threading import Thread, Event, Timer
from DataBase.class_DB import DB
from DataBase.class_alarm import Alarm
from common.class_json import *
from CODE.class_message_search import TimeSetting
import select
import re
import datetime


class Server:
    # HOST = '10.10.20.115'
    HOST = '127.0.0.1'
    PORT = 9999
    BUFFER = 50000
    FORMAT = "utf-8"
    HEADER_LENGTH = 30

    log_in = "log_in"
    join_user = "join_user"
    send_chatbot = "send_chatbot"
    send_all = "send_all"
    time_to_alarm = "time_to_alarm"
    user_alarm_list = "user_alarm_list"

    pass_encoded = "pass"
    dot_encoded = "."

    def __init__(self, db_conn: DB, time_set: TimeSetting):
        # 서버 소켓 설정
        self.time_set = time_set
        self.db_conn = db_conn
        self.server_socket = None
        self.config = None
        self.sockets_list = list()
        self.clients = dict()
        self.thread_for_run = None
        self.run_signal = True
        self.encoder = ObjEncoder()
        self.decoder = ObjDecoder()

    def set_config(self, configure):
        self.config = configure
        print('서버 설정 적용됨')

    def start(self):
        if self.thread_for_run is not None:  # 실행중이면 종료 시키기
            return
        self.server_socket = socket(AF_INET, SOCK_STREAM)  # AF_INET(ipv4를 의미)
        self.server_socket.bind((self.HOST, self.PORT))  # 바인딩
        self.server_socket.listen()  # 리슨 시작
        self.sockets_list.clear()  # 소켓리스트 클리어
        self.sockets_list.append(self.server_socket)
        self.run_signal = True
        self.thread_for_run = Thread(target=self.run)
        self.thread_for_run.start()
        # 이미 기간이 지난 알람 지우기 및 알람 시그널 보내주기
        self.thread_alarm_signal = Thread(target=self.alarm_signal)
        self.thread_alarm_signal.start()

    def stop(self):
        self.run_signal = False
        if self.thread_for_run is not None:
            self.thread_for_run.join()
        self.server_socket.close()
        self.thread_for_run = None

    def run(self):
        while True:
            if self.run_signal is False:
                break
            try:
                read_sockets, _, exception_sockets = select.select(self.sockets_list, [], self.sockets_list, 0.1)
            except Exception:
                continue
            for notified_socket in read_sockets:
                if notified_socket == self.server_socket:
                    client_socket, client_address = self.server_socket.accept()
                    # user = self.receive_message(client_socket)
                    # if user is False:
                    #     continue
                    self.sockets_list.append(client_socket)
                    # self.clients[client_socket] = user

                else:
                    message = self.receive_message(notified_socket)

                    if message is False:
                        self.sockets_list.remove(notified_socket)
                        # del self.clients[notified_socket]
                        continue

            for notified_socket in exception_sockets:
                self.sockets_list.remove(notified_socket)
                del self.clients[notified_socket]

    # 1분 마다 돌고 알람이 울릴 시간이 되면 클라이언트한태 정보를 보냄
    def alarm_signal(self):
        now_sec = datetime.datetime.today().strftime('%S')
        print(datetime.datetime.now())
        if now_sec == "00":
            # 알람 시간 확인
            now_time = datetime.datetime.today().strftime('%H:%M')
            now_date = datetime.datetime.today().strftime('%m.%d')
            now_week = datetime.datetime.today().weekday()
            # 알람 정보 찾아오기
            alarm_info = self.db_conn.search_alarm(now_week, now_time)
            for i in alarm_info:
                header_msg = self.time_to_alarm
                data_obj = self.encoder.toJSON_as_binary(i)
                return_result = self.fixed_volume(header_msg, data_obj)
                for client_socket in self.sockets_list:
                    if self.server_socket != client_socket:
                        client_socket.send(return_result)
            # 현재시간보다 뒤에있는 알람들 다 삭제
            self.db_conn.before_del_alarm(now_date, now_time)
            # 60초 뒤에 쓰레드 다시 돌리기
            threading.Timer(60, self.alarm_signal).start()
        elif now_sec == "01":
            # 알람 시간 확인
            now_time = datetime.datetime.today().strftime('%H:%M')
            now_date = datetime.datetime.today().strftime('%m.%d')
            # 알람 정보 찾아오기
            alarm_info = self.db_conn.search_alarm(now_date, now_time)
            # 현재시간보다 뒤에있는 알람들 다 삭제
            self.db_conn.before_del_alarm(now_date, now_time)
            threading.Timer(59, self.alarm_signal).start()
        else:
            threading.Timer(1, self.alarm_signal).start()

    # 클라이언트로 정보 전달
    def send_message(self, client_socket: socket, result_):
        client_socket.send(result_)

    # 규격 맞춰주기
    def fixed_volume(self, header, data):
        header_msg = f"{header:<{self.HEADER_LENGTH}}".encode(self.FORMAT)
        data_msg = f"{data:<{self.BUFFER - self.HEADER_LENGTH}}".encode(self.FORMAT)
        return header_msg + data_msg

    def receive_message(self, client_socket: socket):
        try:
            recv_message = client_socket.recv(self.BUFFER)
            request_header = recv_message[:self.HEADER_LENGTH].strip().decode(self.FORMAT)
            request_data = recv_message[self.HEADER_LENGTH:].strip().decode(self.FORMAT)
            print(f"Server RECEIVED: ({request_header},{request_data})")
            print(request_header)
            print(type(request_header))
        except:
            return False

        # 로그인
        if request_header == self.log_in:
            object_ = self.decoder.binary_to_obj(request_data)
            result_ = self.db_conn.user_log_in(object_.user_id, object_.user_pw)
            if result_ is False:
                response_header = self.log_in
                response_data = self.dot_encoded
                return_result = self.fixed_volume(response_header, response_data)
                self.send_message(client_socket, return_result)
            else:
                response_header = self.log_in
                response_data = self.encoder.toJSON_as_binary(result_)
                return_result = self.fixed_volume(response_header, response_data)
                self.send_message(client_socket, return_result)

        # 회원가입
        elif request_header == self.join_user:
            object_ = self.decoder.binary_to_obj(request_data)
            result_ = self.db_conn.user_sign_up(object_.user_id, object_.user_pw, object_.user_nickname)
            response_header = self.join_user
            return_result = self.fixed_volume(response_header, result_)
            self.send_message(client_socket, return_result)

        elif request_header == self.send_chatbot:
            object_ = self.decoder.binary_to_obj(request_data)
            response_header = self.send_chatbot
            if '삭제' in object_.send_msg and '수정' in object_.send_msg:
                return_msg = '요청을 하나만 해주시길 바랍니다.'
            elif '삭제' in object_.send_msg:
                return_msg = self.time_set.alarm_del(object_)
            elif '수정' in object_.send_msg:
                return_msg = self.time_set.alarm_change(object_)
            else:
                return_msg = self.time_set.alarm_setting_info(object_)
            # 여기서 함수로 메시지 정보를 넘길꺼임 그리고 리턴으로 값을 받음
            print(return_msg)
            return_result = self.fixed_volume(response_header, return_msg)
            self.send_message(client_socket, return_result)

        # 전체 채팅
        elif request_header == self.send_all:
            response_header = self.send_all
            socket_list = self.sockets_list.copy()
            socket_list.remove(self.server_socket)
            socket_list.remove(client_socket)
            for socket_ in socket_list:
                return_result = self.fixed_volume(response_header, request_data)
                self.send_message(socket_, return_result)

        # 유저가 설정한 알람 정렬된 상태로 정보 보내기
        elif request_header == self.user_alarm_list:
            response_header = self.user_alarm_list
            object_ = self.decoder.binary_to_obj(request_data)
            alarm_list = self.db_conn.search_user_setting_alarm(object_)
            result_ = self.encoder.toJSON_as_binary(alarm_list)
            return_result = self.fixed_volume(response_header, result_)
            self.send_message(client_socket, return_result)
