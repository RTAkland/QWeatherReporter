#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: markushammered@gmail.com
# @Development Tool: PyCharm
# @Create Time: 2021/9/29
# @File Name: API_get_warning_list.py:

"""
开发版key使用此API可以快速返回正在预警的城市id
Only Dev-mode
"""

import requests
import json
from ruamel.yaml import YAML


def get_warning_list(_range='cn'):
    yaml = YAML()
    with open('./config.yml', 'r', encoding='utf-8') as f:
        config = yaml.load(f.read())
        key = config['request-settings']['key']
    session = requests.Session()
    session.trust_env = False
    r = session.get(f'https://devapi.qweather.com/v7/warning/list?range={_range}&key={key}')
    _data = json.loads(r.text)
    return _data['code'], _data['warningLocList'][0]['locationId']
