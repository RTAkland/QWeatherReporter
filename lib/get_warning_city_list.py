#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Author: markushammered@gmail.com
# @Development Tool: PyCharm
# @Create Time: 2021/9/29
# @File Name: API_get_warning_list.py:

"""
开发版key使用此API可以快速返回正在预警的城市id
启用等级: DEV
"""

from core.read_config import read_config
import requests
import json


def get_warning_list(_range='cn'):
    """
    获取当前正在发送自然灾害的城市id列表
    :param _range: Range
    :return:
    """
    settings = read_config()
    key = settings[1]['key']
    r = requests.get(f'https://devapi.qweather.com/v7/warning/list?range={_range}&key={key}')
    _data = json.loads(r.text)
    return _data['code'], _data['warningLocList'][0]['locationId']
