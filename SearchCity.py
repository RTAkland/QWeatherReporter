#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: markushammered@gmail.com
# @Development Tool: PyCharm
# @Create Time: 2021/10/9
# @File Name: SearchCity.py


import getpass
import time
import sys
import pandas as pd
import logging

from ruamel.yaml import YAML
from colorlog import ColoredFormatter


def read_excel(kw: str):
    """
    读取城市列表并根据传入的参数进行搜索
    :param kw: 进行匹配的关键字
    :return: city_list
    """
    index_count = 0
    city_list = []
    logger.info('文件读取中...')
    df = pd.read_excel('./resource/China-City-List.xlsx')
    pd.set_option('max_rows', None)  # 读取xlsx文件不折叠
    data_records = df.to_dict(orient='split')
    for i in data_records['data']:
        if kw in str(i):
            print(
                f'\033[32;32m[{time.strftime("%H:%M:%S", time.localtime())}] [INFO] {index_count} {i[2]}-{i[4]}-{i[6]}')
            index_count += 1
            city_list.append(i)
    if not city_list:
        return False
    return city_list


if __name__ == '__main__':
    logger = logging.getLogger("autotest")
    logger.setLevel(logging.DEBUG)
    fmt = "%(log_color)s[%(asctime)s] [%(log_color)s%(levelname)s] %(log_color)s%(message)s"
    dateformat = '%H:%M:%S'

    formatter = ColoredFormatter(fmt=fmt, datefmt=dateformat, reset=True, secondary_log_colors={}, style='%')
    hd_1 = logging.StreamHandler()
    hd_1.setFormatter(formatter)
    logger.addHandler(hd_1)
    yaml = YAML()

    keyword = input(f'\033[32;32m[{time.strftime("%H:%M:%S", time.localtime())}] [INFO] 输入城市名进行搜索:')
    if keyword:
        result = read_excel(keyword)
        if result:
            try:
                select_index = int(
                    input(f'\033[32;32m[{time.strftime("%H:%M:%S", time.localtime())}] [INFO] 请输入数据前的索引选择城市:'))
                with open('./config.yml', 'r', encoding='utf-8') as of:
                    data = yaml.load(of)
                    data['request-settings']['location'] = result[select_index][0]
                    data['only-view-settings'][
                        'city-name'] = f'{result[select_index][2]}-{result[select_index][4]}-{result[select_index][6]} '
                    data['only-view-settings']['time'] = time.strftime("%a %b %d %H:%M:%S %Y", time.localtime())
                    data['only-view-settings']['user'] = getpass.getuser()
                with open('./config.yml', 'w', encoding='utf-8') as wf:
                    yaml.dump(data, wf)
                logger.info('写入完成')
                sys.exit(0)
            except ValueError or IndexError:
                logger.error('请输入正确的索引')
                sys.exit(1)
        else:
            logger.error('无搜索结果')
            sys.exit(1)
    else:
        logger.error('无搜索结果')
        sys.exit(1)
