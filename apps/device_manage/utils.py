# -*- coding:utf-8 -*-
"""
@Describe: utils
@Author: zhongxin
@Time: 2019-12-06 21:35
@File: utils.py
@Email: 490336534@qq.com
"""
from utils.timeoperator import change_time


def get_count_by_device_info(datas):
    datas_list = []
    for item in datas:
        item['create_time'] = change_time(item['create_time'])
        datas_list.append(item)
    return datas_list
