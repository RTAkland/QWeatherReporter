#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Author: markushammered@gmail.com
# @Development Tool: PyCharm
# @Create Time: 2021/9/29
# @File Name: get_location.py


import requests
import json


class Request(object):
    def __init__(self):
        self.url1 = 'https://ip.tool.lu'
        self.url2 = 'https://acg.toubiec.cn/random.php?ret=json'
        self.session = requests.Session()
        self.session.trust_env = False

    def request_way_1(self):
        """
        https://ip.tool.lu
        :return: {'IP:': r.split(':')[1].split()[0], 'Location': r.split(':')[2].split()}
        """
        r = self.session.get(self.url1, timeout=5).text
        return {'IP:': r.split(':')[1].split()[0], 'Location': r.split(':')[2].split()}  # return IP & Cities

    def request_way_2(self):
        """
        https://acg.toubiec.cn/random.php?ret=json
        :return: {'IP': data['client_ip'], 'Location': data['client_lsp']}
        """
        r = self.session.get(self.url2, timeout=5).text
        data = json.loads(r)[0]
        return {'IP': data['client_ip'], 'Location': data['client_lsp']}


