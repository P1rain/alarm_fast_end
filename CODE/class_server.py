import os
from multiprocessing import Process
from socket import *
from threading import Thread, Event
from DataBase.class_DB import DB
from common.class_json import *
import select
import re
import datetime


class Server:
    HOST = '127.0.0.1'
    PORT = 9999
    BUFFER = 50000
    FORMAT = "utf-8"
    HEADER_LENGTH = 30

    log_in = "log_in"
    join_user = "join_user"
    send_chatbot = "send_chatbot"
    send_all = "send_all"

    pass_encoded = "pass"
    dot_encoded = "."

    def __init__(self, db_conn: DB):
        # 서버 소켓 설정
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

    # 클라이언트로 정보 전달
    def send_message(self, client_socket: socket, result_):
        client_socket.send(result_)

    # 규격 맞춰주기
    def fixed_volume(self, header, data):
        header_msg = f"{header:<{self.HEADER_LENGTH}}".encode(self.FORMAT)
        data_msg = f"{data:<{self.BUFFER - self.HEADER_LENGTH}}".encode(self.FORMAT)
        return header_msg + data_msg

    # 메시지에서 요일 찾기
    def alarm_day_of_the_week(self, rerequest_data):
        day_of_the_week_list = ['일요일', '월요일', '화요일', '수요일', '목요일', '금요일', '토요일']
        msg = rerequest_data.replace(' ', '')


    # 메시지 내용에서 정보 뽑아오기
    def alarm_time_data(self, rerequest_data):
        msg = rerequest_data.replace(' ', '')
        now = datetime.datetime.now()
        now_hour = int(now.hour)
        now_minute = int(now.minute)
        # : 의 앞뒤로 값이 들어간 경우의 시간확인
        if len(re.findall(r'\d+:\d+', msg)) == 1:
            time_int = re.findall(r'\d+:\d+', msg)
            time_cut = re.split(r'[:]', time_int[0])
            hour = int(time_cut[0])
            minute = int(time_cut[1])
            # 정상적으로 시간이 들어왔나
            if hour < 24:
                # 현재시간과 알람 설정 시간 비교
                if hour < now_hour:
                    set_date = now + datetime.timedelta(days=1)
            else:
                return False, False
            if minute < 60:
                if (minute < now_minute) and (hour == now_hour):
                    set_date = now + datetime.timedelta(days=1)
                set_day = set_date.strftime("%m.%d")

                return set_day, time_cut[0] + ":" + time_cut[1]
            else:
                return False, False
        # : 의 앞에만 값이 적혀있는 경우
        elif len(re.findall(r'\d+:', msg)) == 1:
            minute = "00"
            time_int = re.findall(r'\d+:', msg)
            time_cut = re.split(r'[:]', time_int[0])
            hour = int(time_cut[0])
            if hour < 24:
                # 현재시간과 알람 설정 시간 비교
                if hour < now_hour:
                    set_date = now + datetime.timedelta(days=1)
                else:
                    set_date = now
                set_day = set_date.strftime("%m.%d")
                return set_day, time_cut[0] + ":" + minute
            else:
                return False, False
        # 채팅 내용중 시, 분으로 적은 내용이 있을경우 출력시킴
        elif (len(re.findall(r'\d+(시|분)', msg)) == 2) and (len(re.findall(r'\d+(?=시|분)', msg)) == 2) and \
                ('시' in re.findall(r'\d+(시|분)', msg)) and ('분' in re.findall(r'\d+(시|분)', msg)):
            time_str = re.findall(r'\d+(시|분)', msg)
            time_num = re.findall(r'\d+(?=시|분)', msg)
            for j, k in zip(time_str, time_num):
                if (j == '분') and (int(k) < 60):
                    minute = k
                elif j == '분':
                    return False, False
                if (j == '시') and (int(k) < 24):
                    hour = k
                elif j == '시':
                    return False, False
            # 현재시간과 알람 설정 시간 비교
            if int(hour) < now_hour:
                set_date = now + datetime.timedelta(days=1)
            else:
                set_date = now
            if (int(minute) < now_minute) and (int(hour) == now_hour):
                set_date = now + datetime.timedelta(days=1)
            set_day = set_date.strftime("%m.%d")
            return set_day, hour + ":" + minute
        # 시, 분을 적은것이 아닌 시간만 적은 경우
        elif (len(re.findall(r'\d+(시)', msg)) == 1) and ('시' in re.findall(r'\d+(시)', msg)):
            time_num = re.findall(r'(\d+)시', msg)
            if int(time_num[0]) < 24:
                if int(time_num[0]) <= now_hour:
                    set_date = now + datetime.timedelta(days=1)
                else:
                    set_date = now
                set_day = set_date.strftime("%m.%d")
                return set_day, time_num[0] + ':00'
            else:
                return False, False


        else:
            return False, False

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
                response_data = self.FALSE
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

        # 메시지 내용 알람화
        elif request_header == self.alarm_setting:
            object_ = self.decoder.binary_to_obj(request_data)
            day, time = self.alarm_time_data(object_.send_msg)
            print(day, time)
