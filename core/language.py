#!/usr/bin/env python3
# -- coding:utf-8 --
# @Author: markushammered@gmail.com
# @Development Tool: PyCharm
# @Create Time: 2021/12/15
# @File Name: language.py

from ruamel.yaml import YAML
import json


def Language():
    with open('./config.yml', 'r', encoding='utf-8') as lang:
        config = YAML().load(lang.read())
        language_sel = config['client-settings']['language']
        if language_sel not in ['zh_cn', 'en_us']:
            language_sel = 'zh_cn'

    # 打开语言json文件
    with open(f'./res/lang/{language_sel}.json', 'r', encoding='utf-8') as lang_f:
        language = json.loads(lang_f.read())

    return language
