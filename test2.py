import datetime
import re

# import re
#
# a = '7.31일 살려주세요'
# b = '7.21 죽을것 같습니다'
# c = '7-26일 졸리다'
# d = '7/26 성공을 향하여'
# e = '7월 28일3125 끝내자'
# f = '728 끝내자'
# g = '7-26일 졸리다'
# h = '7/26일 졸리다'
#
# list_str = [a, b, c, d, e, f]
# for i in list_str:
#     msg = i.replace(" ", "")
#     day_str1 = re.findall(r'\d+\.\d+', msg)
#     day_cut1 = re.split(r'[월]', day_str1[0])
#     day_str2 = re.findall(r'\d+(월|일)', msg)
#     day_num2 = re.findall(r'\d+(?=월|일)', msg)
#     print(1, day_str1)
#     print(2, day_cut1)

# a = '71시간 후에 아니 12시간 뒤에 알람 설정해줘'
#
# msg = a.replace(" ", "")
#
# print(msg)
#
# test_1 = re.findall(r'\d+(?=시간후)|\d+(?=시간뒤)', msg)
# test_2 = re.findall(r'\d+분후|\d+분뒤', msg)
# print(test_1)

# if "04" < "24":
#     print(1)
# else:
#     print(2)

# today = datetime.datetime.today()
# print(today.weekday())
#
# tomorrow = today + datetime.timedelta(days=1)
# print(tomorrow.weekday())

# day_of_the_week_list = ['월요일', '화요일', '수요일', '목요일', '금요일', '토요일', '일요일']
#
# a = '오늘은 정말 미칠것같은 토요일이에요'
#
# a = re.findall(r'\w요일', a)
# print(a)


if '월요일' < '12.31':
    print(1)
else:
    print(2)