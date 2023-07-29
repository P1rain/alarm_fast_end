import os
import select
import re
import datetime

from DataBase.class_DB import DB
from DataBase.class_alarm import Alarm


class TimeSetting:
    def __init__(self, db_conn: DB):
        self.db_conn = db_conn
        self.day_of_the_week_list = ['월요일', '화요일', '수요일', '목요일', '금요일', '토요일', '일요일']

    # 메시지 해석해서 리턴값은 메시지로 돌려준다고 생각한다.
    def msg_interpret_data(self, object_):
        # db로 알람 정보를 넘길때 필요한 정보를 object형태로 넘길때 필요한 값들을 가지고있음
        self.object_ = object_
        now = datetime.datetime.now()
        self.now = now
        self.now_hour = int(now.hour)
        self.now_minute = int(now.minute)
        send_msg = object_.send_msg
        msg = send_msg.replace(' ', '')
        many_time = '설정할 시간을 하나만 적어주시길 바랍니다.'
        no_time = '설정할 시간을 작성하지 않으셨습니다.'
        week_over = '설정할 요일을 하나만 적어주세요'

        # : 의 앞뒤로 값이 들어간 경우의 시간확인
        if (len(re.findall(r'\d+:\d+', msg)) == 1) and (len(re.findall(r'\d+:', msg)) > 1):
            return many_time

        elif len(re.findall(r'\d+:\d+', msg)) == 1:
            time_int = re.findall(r'\d+:\d+', msg)
            time_cut = re.split(r'[:]', time_int[0])
            week_check = re.findall(r'\w요일', msg)
            # 요일 정보
            if (len(week_check) == 1) and (week_check[0] in self.day_of_the_week_list):
                day_of_the_week = self.day_of_the_week_list.index(week_check[0])
                data_msg = self.alarm_setting_time_day_of_the_week(day_of_the_week, time_cut[0], time_cut[1])
                return data_msg
            elif len(week_check) > 1:
                return week_over
            else:
                data_msg = self.alarm_setting_time_only(time_cut[0], time_cut[1])
                return data_msg

        elif len(re.findall(r'\d+:\d+', msg)) > 1:
            return many_time

        # : 의 앞에만 값이 적혀있는 경우
        elif len(re.findall(r'\d+:', msg)) == 1:
            time_int = re.findall(r'\d+:', msg)
            time_cut = re.split(r'[:]', time_int[0])
            week_check = re.findall(r'\w요일', msg)
            # 요일 정보
            if (len(week_check) == 1) and (week_check[0] in self.day_of_the_week_list):
                day_of_the_week = self.day_of_the_week_list.index(week_check[0])
                data_msg = self.alarm_setting_time_day_of_the_week(day_of_the_week, time_cut[0])
                return data_msg
            elif len(week_check) > 1:
                return week_over
            else:
                data_msg = self.alarm_setting_time_only(time_cut[0])
                return data_msg

        elif len(re.findall(r'\d+:', msg)) > 1:
            return many_time


        # ---------------------------------------------------------------------------------------------
        # 시간후, 시간만 입력한 경우의 형태는 비슷해서 같이 묶어줘야한다
        if len(re.findall('\d+시간후|\d+시간뒤', msg)) == 1:
            after_hour = re.findall('\d+(?=시간후)|\d+(?=시간뒤)', msg)
            data_msg = self.alarm_setting_after_hour_time(int(after_hour[0]))
            return data_msg

        elif len(re.findall('\d+분후|\d+분뒤', msg)) == 1:
            after_minute = re.findall('\d+(?=분후)|\d+(?=분뒤)', msg)
            data_msg = self.alarm_setting_after_minute_time(int(after_minute[0]))
            return data_msg

        # ---------------------------------------------------------------------------------------------------
        # 시,분 형태의 내용
        elif (len(re.findall(r'\d+(시|분)', msg)) == 2) and (len(re.findall(r'\d+(?=시|분)', msg)) == 2) and \
                ('시' in re.findall(r'\d+(시|분)', msg)) and ('분' in re.findall(r'\d+(시|분)', msg)):
            hours_num = re.findall(r'\d+(?=시)', msg)
            minute_num = re.findall(r'\d+(?=분)', msg)
            week_check = re.findall(r'\w요일', msg)
            # 요일 정보
            if (len(week_check) == 1) and (week_check[0] in self.day_of_the_week_list):
                day_of_the_week = self.day_of_the_week_list.index(week_check[0])
                data_msg = self.alarm_setting_time_day_of_the_week(day_of_the_week, hours_num[0], minute_num[0])
                return data_msg
            elif len(week_check) > 1:
                return week_over
            else:
                data_msg = self.alarm_setting_time_only(hours_num[0], minute_num[0])
                return data_msg

        elif (len(re.findall(r'\d+(시|분)', msg)) > 2) and (len(re.findall(r'\d+(?=시|분)', msg)) > 2):
            return many_time

        elif (len(re.findall(r'\d+(시)', msg)) == 1) and ('시' in re.findall(r'\d+(시)', msg)):
            time_num = re.findall(r'\d+(?=시)', msg)
            week_check = re.findall(r'\w요일', msg)
            # 요일 정보
            if (len(week_check) == 1) and (week_check[0] in self.day_of_the_week_list):
                day_of_the_week = self.day_of_the_week_list.index(week_check[0])
                data_msg = self.alarm_setting_time_day_of_the_week(day_of_the_week, time_num[0])
                return data_msg
            elif len(week_check) > 1:
                return week_over
            else:
                data_msg = self.alarm_setting_time_only(time_num[0])
                return data_msg

    # 몇시간뒤,후의 기능
    def alarm_setting_after_hour_time(self, after_hour):
        set_date_time = self.now + datetime.timedelta(hours=after_hour)
        set_day = set_date_time.strftime("%m.%d")
        set_time = set_date_time.strftime("%H:%M")
        weekday = self.now.weekday()
        alarm_data = Alarm(None, self.object_.user_id, set_time, set_day, weekday, None)
        result_ = self.db_conn.alarm_setting(alarm_data)
        if result_ is False:
            return '이미 존재하는 알람입니다.\n다시 시도해주시길 바랍니'
        else:
            user_nickname = self.db_conn.search_nickname(result_.user_id)
            alarm_date = result_.alarm_date
            alarm_day_of_the_week = self.day_of_the_week_list[int(result_.alarm_day_of_the_week)]
            alarm_time = self.converter_time(result_.alarm_time)
            return f'{user_nickname}님의 알람이 {alarm_date}일 {alarm_day_of_the_week}\n{alarm_time}에 맞춰졌습니다.'

    # 몇분뒤, 후의 기능
    def alarm_setting_after_minute_time(self, after_minute):
        set_date_time = self.now + datetime.timedelta(minutes=after_minute)
        set_day = set_date_time.strftime("%m.%d")
        set_time = set_date_time.strftime("%H:%M")
        weekday = self.now.weekday()
        alarm_data = Alarm(None, self.object_.user_id, set_time, set_day, weekday, None)
        result_ = self.db_conn.alarm_setting(alarm_data)
        if result_ is False:
            return '이미 존재하는 알람입니다.\n다시 시도해주시길 바랍니'
        else:
            user_nickname = self.db_conn.search_nickname(result_.user_id)
            alarm_date = result_.alarm_date
            alarm_day_of_the_week = self.day_of_the_week_list[int(result_.alarm_day_of_the_week)]
            alarm_time = self.converter_time(result_.alarm_time)
            return f'{user_nickname}님의 알람이 {alarm_date}일 {alarm_day_of_the_week}\n{alarm_time}에 맞춰졌습니다.'

    # 오직 시간만 입력했을 경우
    def alarm_setting_time_only(self, hours, minutes='00'):
        # 수가 제대로 들어왔는지 확인하기
        if int(hours) > 23:
            return '시간을 잘못 입력하신것 같습니다.\n다시 입력해주시길 바랍니다.'
        if int(minutes) > 59:
            return '시간을 잘못 입력하신것 같습니다.\n다시 입력해주시길 바랍니다.'
        # 숫자 글자수 파악후 추가해주기
        if len(hours) == 1:
            hours = "0" + hours
        if len(minutes) == 1:
            minutes = "0" + minutes
        # 알람 설정한 시간한 시간과 설정할 시간을 비교해서 날짜 정보를 추가해준다.
        if int(hours) < self.now_hour:
            self.now = self.now + datetime.timedelta(days=1)
        if (int(minutes) < self.now_minute) and (int(hours) == self.now_hour):
            self.now = self.now + datetime.timedelta(days=1)
        print(1)
        weekday = self.now.weekday()
        set_day = self.now.strftime("%m.%d")
        alarm_data = Alarm(None, self.object_.user_id, hours+":"+minutes, set_day, weekday, None)
        result_ = self.db_conn.alarm_setting(alarm_data)
        if result_ is False:
            return '이미 존재하는 알람입니다.\n다시 시도해주시길 바랍니'
        else:
            user_nickname = self.db_conn.search_nickname(result_.user_id)
            alarm_date = result_.alarm_date
            alarm_day_of_the_week = self.day_of_the_week_list[int(result_.alarm_day_of_the_week)]
            alarm_time = self.converter_time(result_.alarm_time)
            return f'{user_nickname}님의 알람이 {alarm_date}일\n{alarm_time}에 맞춰졌습니다.'

    def alarm_setting_time_date(self, date, hour, minutes='00'):
        pass

    def alarm_setting_time_day_of_the_week(self, day_of_the_week, hours, minutes='00'):
        # 수가 제대로 들어왔는지 확인하기
        if int(hours) > 23:
            return '시간을 잘못 입력하신것 같습니다.\n다시 입력해주시길 바랍니다.'
        if int(minutes) > 59:
            return '시간을 잘못 입력하신것 같습니다.\n다시 입력해주시길 바랍니다.'
        # 숫자 글자수 파악후 추가해주기
        if len(hours) == 1:
            hours = "0" + hours
        if len(minutes) == 1:
            minutes = "0" + minutes
        alarm_data = Alarm(None, self.object_.user_id, hours+":"+minutes, self.day_of_the_week_list[day_of_the_week], day_of_the_week, None)
        result_ = self.db_conn.alarm_setting(alarm_data)
        if result_ is False:
            return '이미 존재하는 알람입니다.\n다시 시도해주시길 바랍니'
        else:
            user_nickname = self.db_conn.search_nickname(result_.user_id)
            alarm_date = self.day_of_the_week_list[day_of_the_week]
            alarm_time = self.converter_time(result_.alarm_time)
            return f'{user_nickname}님의 알람이 {alarm_date}\n{alarm_time}에 맞춰졌습니다.'


    def converter_time(self, time_data):
        time = time_data
        hour = time_data[:2]
        minute = time_data[3:]
        if hour == "12":
            time = ("오후 " + f'{hour}:{minute}')
        elif hour > "12":
            time = ("오후 " + "0" + f'{int(hour) - 12} : {minute}')
        elif hour < "12":
            time = ("오전 " + f'{hour} : {minute}')
        return time

# 응애
