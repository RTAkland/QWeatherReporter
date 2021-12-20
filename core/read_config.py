#!/usr/bin/env python3
# -- coding:utf-8 --
# @Author: markushammered@gmail.com
# @Development Tool: PyCharm
# @Create Time: 2021/12/15
# @File Name: read_config.py

from ruamel.yaml import YAML


def read_config():
    """
    读取配置文件并返回读取到的内容同
    :return: mail-settings, request-settings, client-settings, only-view-settings --> 0, 1, 2, 3
    """
    config_file = 'config.yml'
    with open(f'./{config_file}', 'r') as conf:
        config = YAML().load(conf.read())
        mail_settings = config['mail-settings']
        request_settings = config['request-settings']
        client_settings = config['client-settings']
        only_view = config['only-view-settings']
    return mail_settings, request_settings, client_settings, only_view

