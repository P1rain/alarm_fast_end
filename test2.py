import re

a = '7.31일 살려주세요'
b = '7.21 죽을것 같습니다'
c = '7-26일 졸리다'
d = '7/26 성공을 향하여'
e = '7월 28일3125 끝내자'
f = '728 끝내자'
g = '7-26일 졸리다'
h = '7/26일 졸리다'

list_str = [a, b, c, d, e, f]
for i in list_str:
    msg = i.replace(" ", "")
    day_str1 = re.findall(r'\d+\.\d+', msg)
    day_cut1 = re.split(r'[월]', day_str1[0])
    day_str2 = re.findall(r'\d+(월|일)', msg)
    day_num2 = re.findall(r'\d+(?=월|일)', msg)
    print(1, day_str1)
    print(2, day_cut1)
