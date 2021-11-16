#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: markushammered@gmail.com
# @Development Tool: PyCharm
# @Create Time: 2021/9/29
# @File Name: API_real_time_air_quality.py

"""
开发版key获取实时空气质量
only: Dev-mode
"""

import requests
import json
import sys
from ruamel.yaml import YAML


def real_time_air_quality():
    yaml = YAML()
    with open(sys.path[1] + '/config.yml', 'r', encoding='utf-8') as f:
        config = yaml.load(f.read())

        mode = config['request-settings']['mode']
        key = config['request-settings']['key']
        location = config['request-settings']['location']
        unit = config['request-settings']['unit']
        lang = config['request-settings']['lang']

    if mode != 'dev':
        return False, print('Only Dev-mode')
    session = requests.Session()
    session.trust_env = False
    r = session.get(f'https://devapi.qweather.com/v7/air/now?'
                    f'location={location}config.yml&key={key}&lang={lang}&unit={unit}&gzip=y')
    _data = json.loads(r.text)

    return _data['code'], _data['now']
