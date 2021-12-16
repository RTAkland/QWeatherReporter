#!/usr/bin/env python3
# -- coding:utf-8 --
# @Author: markushammered@gmail.com
# @Development Tool: PyCharm
# @Create Time: 2021/12/15
# @File Name: read_config.py

from ruamel.yaml import YAML


def read_config():
    """

    :return: mail-settings, request-settings, client-settings --> 0, 1, 2
    """
    with open('./config.yml', 'r') as conf:
        config = YAML().load(conf.read())
        mail_settings = config['mail-settings']
        request_settings = config['request-settings']
        client_settings = config['client-settings']
    return mail_settings, request_settings, client_settings

