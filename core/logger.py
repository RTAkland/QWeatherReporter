#!/usr/bin/env python3
# -- coding:utf-8 --
# @Author: markushammered@gmail.com
# @Development Tool: PyCharm
# @Create Time: 2021/12/15
# @File Name: logger.py

from colorlog import ColoredFormatter
import logging.handlers
import time

date_format = '%H:%M:%S'
info_format_console = '%(log_color)s[%(asctime)s] |%(levelname)-8s |%(lineno)-3s |%(message)s'
info_format_file = '[%(asctime)s] |%(levelname)-8s |%(lineno)-3s |%(funcName)s |%(pathname)s |%(message)s'
formatter = ColoredFormatter(fmt=info_format_console,
                             datefmt=date_format,
                             reset=True,
                             log_colors={
                                 'DEBUG': 'light_purple',
                                 'INFO': 'light_cyan',
                                 'WARNING': 'yellow',
                                 'ERROR': 'red',
                                 'CRITICAL': 'red,bold_red'})
formatter_file = logging.Formatter(fmt=info_format_file,
                                   datefmt=date_format)

Logger = logging.getLogger('MainLogger')
Logger.setLevel(logging.DEBUG)
ConsoleLogger = logging.StreamHandler()  # 输出到终端
ConsoleLogger.setFormatter(formatter)
log_name = time.strftime('%Y-%m-%d#%H')  # 一小时内使用的日志文件都是同一个
FileLogger = logging.handlers.RotatingFileHandler(filename=f'./logs/{log_name}.log',
                                                  maxBytes=102400,
                                                  backupCount=5)  # 每个日志文件最大102400字节(100Kb)
FileLogger.setFormatter(formatter_file)
Logger.addHandler(ConsoleLogger)
Logger.addHandler(FileLogger)

