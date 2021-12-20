#!/usr/bin/env python3
# -- coding:utf-8 --
# @Author: markushammered@gmail.com
# @Development Tool: PyCharm
# @Create Time: 2021/10/31
# @File Name: API_indices.py

"""
获取生活建议的API
获取所有生活建议 (15+)
启用等级: DEV
"""

from core.read_config import read_config
import requests
import json


def indices():
    """
    获取生活建议
    :return:
    """
    settings = read_config()
    location = settings[1]['location']
    key = settings[1]['key']
    lang = settings[1]['lang']
    unit = settings[1]['unit']
    r = requests.get(
        f'https://devapi.qweather.com/v7/indices/1d?type=0&location={location}&key={key}&lang={lang}&unit={unit}')
    data = json.loads(r.text)
    status_code = data['code']
    updateTime = str(data['updateTime'][:-6]).replace('T', '')
    main_data = data['daily']  # 1-15(+)
    return status_code, updateTime, main_data

