# -- coding:utf-8 --
# @Author: markushammered@gmail.com
# @Development Tool: PyCharm
# @Create Time: 2021/12/24
# @File Name: hitokoto.py

import requests
from core.language import Language
from core.logger import Logger


def hitokoto():
    language = Language()
    url = 'https://v1.hitokoto.cn/'
    Logger.info(f'{language["hitokoto"]}')
    res = requests.get(url).json()
    speaker = res['from_who']
    text = res['hitokoto']
    if not speaker:
        speaker = language['noname']
    full_text = f'{text}  --{speaker}'

    return full_text
