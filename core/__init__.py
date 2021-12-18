#!/usr/bin/env python3
# -- coding:utf-8 --
# @Author: markushammered@gmail.com
# @Development Tool: PyCharm
# @Create Time: 2021/12/15
# @File Name: __init__.py

"""
Check the configuration file
"""

import os
import sys
from core.logger import Logger
from core.language import Language
from core.read_config import read_config

Logger.info('Be imported')

settings = read_config()

if not os.path.exists('./logs'):
    os.mkdir('./logs')

for mail in settings[0].values():
    if not mail:
        Logger.critical('mail-settings 有未填写项目')
        sys.exit(1)
for request in settings[1].values():
    if not request:
        Logger.critical('request-settings 有未填写项目')
        sys.exit(1)
for other in settings[1].values():
    if not other:
        Logger.critical('client-settings 有未填写项目')
        sys.exit(1)
