#!/usr/bin/env python3
# -- coding:utf-8 --
# @Author: markushammered@gmail.com
# @Development Tool: PyCharm
# @Create Time: 2021/12/15
# @File Name: read_excel.py

import pandas
from core.logger import Logger
from core.language import Language


def read_excel(kw: str):
    """
    读取china_city_list.xlsx并搜索匹配关键字的结果并输出到终端
    :param kw: keyword
    :return: city_list
    """

    language = Language()
    index_count = 0
    city_list = []
    Logger.info(f'[Search]{language["reading_the_file"]}')
    df = pandas.read_excel(f'./res/china_city_list.xlsx')
    pandas.set_option('max_rows', None)  # 读取xlsx文件不折叠
    data_records = df.to_dict(orient='split')
    for i in data_records['data']:
        if kw in str(i):
            Logger.info(f' {index_count} | {i[2]}-{i[4]}-{i[6]}')
            city = [index_count, i[0], i[1], i[2], i[3], i[4], i[5], i[6], i[7], i[8], i[9]]
            index_count += 1
            city_list.append(city)
    return city_list
