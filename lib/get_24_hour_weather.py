#!/usr/bin/env python3
# -- coding:utf-8 --
# @Author: markushammered@gmail.com
# @Development Tool: PyCharm
# @Create Time: 2021/10/31
# @File Name: API_24hour_weathers.py

"""
获取未来24小时时级天气预报 (24)
启用等级: DEV
"""

from core.read_config import read_config
import requests
import json


def hourly_weather():
    """
    获取24小时的天气
    :return:
    """
    settings = read_config()
    location = settings[1]['location']
    key = settings[1]['key']
    lang = settings[1]['lang']
    unit = settings[1]['unit']
    r = requests.get(
        f'https://devapi.qweather.com/v7/weather/24h?location={location}&key={key}&lang={lang}&unit={unit}')
    data = json.loads(r.text)

    status_code = data['code']
    updateTime = str(data['updateTime'][:-6])[10:].replace('T', '')
    main_data = data['hourly']  # 24
    return status_code, updateTime, main_data

