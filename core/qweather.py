#!/usr/bin/env python3
# -- coding:utf-8 --
# @Author: markushammered@gmail.com
# @Development Tool: PyCharm
# @Create Time: 2021/12/15
# @File Name: qweather.py


import sys
import time
import argparse
from concurrent.futures import ProcessPoolExecutor
from core.logger import Logger
from core.language import Language
from core.settings import change_settings
from core.read_config import read_config
from core.sendmail import Mail
from lib.webservice import accept_requests

language = Language()
settings = read_config()
processes = ProcessPoolExecutor(max_workers=3)


def check_time():
    """
    通过多进程让函数和主程序并行,
    并持续检测本地计算机时间是否和配置文件内填写的发送时间一致
    :return:
    """
    mode = settings[1]['mode']
    time_list = settings[2]['send-times']
    match mode:
        case 'dev':
            while True:
                local_time = time.strftime("%H:%M", time.localtime())
                time.sleep(1)
                if local_time in time_list:
                    Mail().dev_version()
                    Logger.info(f'{language["mail_succeed"]}')
                    Logger.info(f'{language["wait_seconds"]}')
                    time.sleep(60)
        case 'free':
            while True:
                local_time = time.strftime("%H:%M", time.localtime())
                time.sleep(1)
                if local_time in time_list:
                    Mail().free_version()
                    Logger.info(f'{language["mail_succeed"]}')
                    Logger.info(f'{language["wait_seconds"]}')
                    time.sleep(60)


def check_config():
    """
    返回配置文件中的location项是否填写
    :return: True or False
    """
    location = settings[1]['location']
    if location:
        return True
    else:
        return False


def setting():
    """
    检查配置文件是否填写完成
    :return:
    """
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


def main():
    """
    主程序
    :return:
    """

    Logger.info(f'{language["statement_1"]}')
    Logger.info(f'{language["statement_2"]}')
    Logger.info(f'{language["statement_3"]}')
    Logger.info(f'{language["statement_4"]}')

    parser = argparse.ArgumentParser()
    arg_keywords = ['free', 'dev', 'warning', 'setting']
    parser.add_argument('-t',
                        '--test',
                        help='Some operations for test.',
                        choices=arg_keywords)
    startup_arg = parser.parse_args().test

    match startup_arg:
        case 'free':
            Mail().free_version()
            Logger.debug(f'{language["debug_done"]}')
            sys.exit(0)
        case 'dev':
            Mail().dev_version()
            Logger.debug(f'{language["debug_done"]}')
            sys.exit(0)
        case 'warning':
            Mail().warning_()
            Logger.debug(f'{language["debug_done"]}')
            sys.exit(0)
        case 'setting':
            change_settings()
            Logger.debug(f'{language["debug_done"]}')
        case _:
            if check_config():
                setting()
            else:
                change_settings()

    processes.submit(check_time)
    if settings[2]['webservice']:
        Logger.info(f'{language["webservice_ip"]}:127.0.0.1:7898')
        processes.submit(accept_requests())

    time_count = 0
    while True:
        time_count += 1
        time.sleep(1)
        if time_count == 600:
            Mail().warning_()
            time_count = 0
