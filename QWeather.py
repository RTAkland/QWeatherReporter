#!/usr/bin/env python3
# -- coding:utf-8 --
# @Author: markushammered@gmail.com
# @Development Tool: PyCharm
# @Create Time: 2021/12/16
# @File Name: QWeather.py


import sys
from core import qweather
from core.logger import Logger

if __name__ == '__main__':
    Logger.info('Start')
    sys.exit(qweather.main())
