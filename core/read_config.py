#!/usr/bin/env python3
# -- coding:utf-8 --
# @Author: markushammered@gmail.com
# @Development Tool: PyCharm
# @Create Time: 2021/12/15
# @File Name: read_config.py

from ruamel.yaml import YAML
from core.language import Language
from core.logger import Logger


def read_config():
    """

    :return: config
    """
    language = Language()
    with open('./config.yml', 'r') as conf:
        config = YAML().load(conf.read())
        Logger.info(language['config_file_read_successfully'])
    return config

