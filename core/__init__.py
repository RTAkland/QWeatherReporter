#!/usr/bin/env python3
# -- coding:utf-8 --
# @Author: markushammered@gmail.com
# @Development Tool: PyCharm
# @Create Time: 2021/12/15
# @File Name: __init__.py

"""
Check the configuration file
"""

import sys
from ruamel.yaml import YAML
from core.logger import Logger
from core.language import Language


with open('./config.yml', 'r') as f:
    settings = YAML().load(f.read())

for mail in settings['mail-settings'].values():
    if not mail:
        Logger.critical('mail-settings 有未填写项目')
        sys.exit(1)
for request in settings['request-settings'].values():
    if not request:
        Logger.critical('request-settings 有未填写项目')
        sys.exit(1)
for other in settings['client-settings'].values():
    if not other:
        Logger.critical('client-settings 有未填写项目')
        sys.exit(1)
