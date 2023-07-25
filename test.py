import re

a = '알람을 25시30분에 맞춰줘'
d = '알람을 5시30 분에 맞춰줘'
e = '알람을 5시 30분에 맞춰줘'
g = '알람을 5시 30 분에 맞춰줘'
c = '알람을 5시 30분에 맞춰줘'
b = '알람을 5 시30분에 맞춰줘'
f = '알람을 5 시 30분에 맞춰줘'
h = '알람을 5 시30 분에 맞춰줘'
i = '알람을 5 시 30 분에 맞춰줘'

str_list = [a, b, c, d, e, f, g, h, i]
hour_list = list()

for i in range(1, 25):
    hour_list.append(f"{i}")
print(hour_list)
for i in str_list:
    test = re.findall('\d+', i)
    if len(test) != 0:
        if test[0] in hour_list:
            print('시간')

