#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: markushammered@gmail.com
# @Development Tool: PyCharm
# @Create Time: 2021/9/29
# @File Name: get_location.py


import requests


def request():
    session = requests.Session()
    session.trust_env = False
    r = session.get('https://ip.tool.lu/', timeout=5).text
    return {'IP:': r.split(':')[1].split()[0], 'Location': r.split(':')[2].split()}  # return IP & Cities
