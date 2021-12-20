#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Author: markushammered@gmail.com
# @Development Tool: PyCharm
# @Create Time: 2021/9/29
# @File Name: API_real_time_air_quality.py

"""
开发版key获取实时空气质量
启用等级: DEV
"""

from core.read_config import read_config
import requests
import json


def real_time_air_quality():
    """
    获取实时的空气质量数据
    :return:
    """
    settings = read_config()
    location = settings[1]['location']
    key = settings[1]['key']
    lang = settings[1]['lang']
    unit = settings[1]['unit']

    r = requests.get(f'https://devapi.qweather.com/v7/air/now?'
                     f'location={location}&key={key}&lang={lang}&unit={unit}&gzip=y')
    _data = json.loads(r.text)

    return _data['now']
