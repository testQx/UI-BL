# def find_element1(*element):
#     print(*element)
#     print(f"{element}")
#
# def find_element2(element):
#     print(*element)
#     print(f"{element}")
#
# find_element1(("tes1", "//*[@id='username']"))
# print("*"*30)
# find_element1(*("tes1", "//*[@id='username']"))
# print("*"*30)
# find_element2(("tes1", "//*[@id='username']"))
import random
import string
import sys
from datetime import timedelta, datetime

import xeger


def get_rand_mac():
    mac = [0x00, 0x16, 0x3e,
           random.randint(0x00, 0x7f),
           random.randint(0x00, 0xff),
           random.randint(0x00, 0xff)]
    return ':'.join(map(lambda x: "%02x" % x, mac))


print(get_rand_mac())


def get_time_stamp(delta=0, delta_type='h', time_format='%Y-%m-%dT%H:%M:%SZ'):
    """
    获取时间戳
    :param delta: 要增加或者减少的时间
    :param delta_type: 单位 d:天 h:小时 m:分钟 s:秒
    :param time_format: 显示格式
    :return:
    """
    if delta_type == 'h':
        delta_time = timedelta(hours=delta)
    elif delta_type == 'm':
        delta_time = timedelta(minutes=delta)
    elif delta_type == 's':
        delta_time = timedelta(seconds=delta)
    elif delta_type == 'd':
        delta_time = timedelta(days=delta)
    else:
        delta_time = 0
    time_stamp = datetime.utcnow() + delta_time
    return time_stamp.strftime(time_format)


print(get_time_stamp())

#
# def get_serial_number(model='IR900'):
#     rules = {
#         "IR900": '^R[A-Z]9[0-9]{12}',
#         "IR700": '^R[A-Z]7[0-9]{12}',
#         "IR600": '^R[A-Z]6[0-9]{12}',
#         "InDTU": '^D[A-Z]3[0-9]{12}',
#         "EG910L": '^(GF|EG)910[0-9]{10}',
#         "VG710": '^V[A-Z]7[0-9]{12}',
#         "IG902": '^G[A-Z]902[0-9]{10}'
#     }
#     xeger_client = xeger.Xeger()
#     if model.upper() not in rules:
#         print(model.upper())
#         print('请输入正确的机型！仅支持以下机型{}'.format(rules.keys()))
#         sys.exit()
#     else:
#         serial_number = xeger_client.xeger(rules[model.upper()])
#         return serial_number
#
# string.ascii_letters
# print(get_serial_number('IR222'))



def random_string(strings=string.ascii_letters, length=15):
    values = ''.join(random.choices(strings, k=length))
    return values


print(random_string())