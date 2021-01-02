# coding: utf-8
import time


def safe_float(input_num):
    """
    安全返回 Float, 如果数据格式不对，则返回 None
    """
    try:
        ret_val = float(input_num)
    except ValueError:
        ret_val = None

    return ret_val


def date_change(date, interval):
    time_tuple = time.strptime(date, '%Y-%m-%d')
    time_s = time.mktime(time_tuple) + interval * 60 * 60 * 24
    new_date = time.strftime('%Y-%m-%d', time.localtime(time_s))

    return new_date
