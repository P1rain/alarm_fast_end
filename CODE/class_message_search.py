import os
import select
import re
import datetime

from DataBase.class_DB import DB
from DataBase.class_alarm import Alarm


class TimeSetting:
    def __init__(self,  db_conn: DB):
        self.db_conn = db_conn

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
        now = datetime.datetime.now()
        many_time = '설정할 시간을 하나만 적어주시길 바랍니다.'

        # : 의 앞뒤로 값이 들어간 경우의 시간확인
        if (len(re.findall(r'\d+:\d+', msg)) == 1) and (len(re.findall(r'\d+:', msg)) > 1):
            return many_time

        elif len(re.findall(r'\d+:\d+', msg)) == 1:
            time_int = re.findall(r'\d+:\d+', msg)
            time_cut = re.split(r'[:]', time_int[0])
            data_msg = self.alarm_setting_time_only(time_cut[0], time_cut[1])
            return data_msg

        elif len(re.findall(r'\d+:\d+', msg)) > 1:
            return many_time

        # : 의 앞에만 값이 적혀있는 경우
        elif len(re.findall(r'\d+:', msg)) == 1:
            # 함수화
            pass

        elif len(re.findall(r'\d+:', msg)) > 1:
            return many_time

        if (len(re.findall(r'\d+(시|분)', msg)) == 2) and (len(re.findall(r'\d+(?=시|분)', msg)) == 2) and \
                ('시' in re.findall(r'\d+(시|분)', msg)) and ('분' in re.findall(r'\d+(시|분)', msg)):
            pass

        elif (len(re.findall(r'\d+(시|분)', msg)) > 2) and (len(re.findall(r'\d+(?=시|분)', msg)) > 2):
            return many_time

    # 몇분,시간뒤,후의 기능
    def alarm_setting_after_time(self, hour, minutes='00'):
        pass

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
        weekday = self.now.weekday()
        set_day = self.now.strftime("%m.%d")
        alarm_data = Alarm(None, self.object_.user_id, hours+":"+minutes, set_day, weekday, None)
        result_ = self.db_conn.alarm_setting(alarm_data)

    def alarm_setting_time_date(self, date, hour, minutes='00'):
        pass

    def alarm_setting_time_day_of_the_week(self, day_of_the_week, hour, minutes='00'):
        pass



# 응애
# if self.alarm_time[:2] == "12":
#             self.alarm_time = ("오후 " + f'{hour}:{minute}')
#         elif self.alarm_time[:2] > "12":
#             self.alarm_time = ("오후 " + "0" + f'{int(hour) - 12} : {minute}')
#         elif self.alarm_time[:2] < "12":
#             self.alarm_time = ("오전 " + f'{hour} : {minute}')