#!/usr/bin/env python
# -- coding:utf-8 --
# @Author: markushammered@gmail.com
# @Development Tool: PyCharm
# @Create Time: 2021/10/31
# @File Name: API_24hour_weathers.py

"""
获取未来24小时时级天气预报 (24)
启用等级: DEV
"""

import requests
import json


def hourly_weather(location: int, key: str, lang: str = 'zh', unit: str = 'm'):
    r = requests.get(
        f'https://devapi.qweather.com/v7/weather/24h?location={location}&key={key}&lang={lang}&unit={unit}')
    data = json.loads(r.text)

    status_code = data['code']
    updateTime = str(data['updateTime'][:-6]).replace('T', '')
    main_data = data['hourly']  # 24
    return status_code, updateTime, main_data

