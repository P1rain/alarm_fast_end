import re

hour_list = list(range(0, 23))
minute_list = list(range(0, 60))

a = '30시발람을60시30분에30맞춰줘'
d = '알람을 05시30 분에 맞춰줘'
e = '알람을 5시 30분에 맞춰줘'
g = '알람을 5시 30 분에 맞춰줘'
c = '알람을 5시 30분에 맞춰줘'
b = '알람을 5 시30분에 맞춰줘'
f = '알람을 5 시 30분에 맞춰줘'
h = '알람을 5 시30 분에 맞춰줘'
i = '알람을 5 시 30 분에 맞춰줘'

str_list = [a, b, c, d, e, f, g, h, i]
# 이놈이 약간 불안하다 이말이야
# for i in str_list:
#     time_str = re.findall(r'시|분', i)
#     time_int = re.findall(r'\d+', i)
#     for j, k in zip(time_str, time_int):
#         if (j == '분') and (int(k) in minute_list):
#             print(k+j)
#         elif j == '분':
#             print("시간이 잘못 입력되었습니다.")
#         if (j == '시') and (int(k) in hour_list):
#             print(k+j)
#         elif j == '시':
#             print("시간이 잘못 입력되었습니다.")
# for i in str_list:
#     msg = i.replace(' ', '')
#     time_str = re.findall(r'\d+(시|분)', msg)
#     time_num = re.findall(r'\d+(?=시|분)', msg)
#     for j, k in zip(time_str, time_num):
#         if (j == '분') and (int(k) in minute_list):
#             print(k+j)
#         elif j == '분':
#             print("시간이 잘못 입력되었습니다.")
#         if (j == '시') and (int(k) in hour_list):
#             print(k+j)
#         elif j == '시':
#             print("시간이 잘못 입력되었습니다.")
# for i in str_list:
#     msg = i.replace(' ', '')
#     if ('시' in re.findall(r'\d+(시|분)', msg)) and ('분' in re.findall(r'\d+(시|분)', msg)):
#         print(1)
for i in str_list:
    msg = i.replace(' ', '')
    time_str = re.findall(r'\d+(시)', msg)
    if len(time_str) == 1:
        print(time_str)
    else:
        print('시간 하나만 임력하라고!!')


# a = '알람을23:30에 맞춰줘'
# b = '알람을 05:30에 맞춰줘'
# c = '알람을05 :30에 맞춰줘'
# d = '알람을05: 30에 맞춰줘'
# e = '알람을05:30 에 맞춰줘'
# f = '알람을 05 :30에 맞춰줘'
# g = '알람을 05: 30에 맞춰줘'
# h = '알람을 05:30 에 맞춰줘'
# i = '알람을05 : 30에 맞춰줘'
# j = '알람을05 :30 에 맞춰줘'
# k = '알람을05: 30 에 맞춰줘'
#
#
#
# # 손댈일 없다 이말이야
# str_list = [a, b, c, d, e, f, g, h, i, j, k]
# for i in str_list:
#     if len(re.findall(r'\d+:\d+', i)) != 0:
#         time_int = re.findall(r'\d+:\d+', i)
#     if len(time_int) != 0:
#         time_cut = re.split(r'[:]', time_int[0])
#         hour = int(time_cut[0])
#         minute = int(time_cut[1])
#         if hour < 24:
#             print('정상적인 시간입력', hour)
#         else:
#             print('비 정상적인 시간입력', hour)
#         if minute < 60:
#             print('정상적인 분입력', minute)
#         else:
#             print('비 정상적인 분입력', minute)
