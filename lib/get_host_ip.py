# -- coding:utf-8 --
# @Author: markushammered@gmail.com
# @Development Tool: PyCharm
# @Create Time: 2021/12/21
# @File Name: get_host_ip.py

import socket


def get_host_ip():
    """
    查询本机ip地址
    :return: ip
    """
    ip_s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    ip_s.connect(('8.8.8.8', 80))
    ip = ip_s.getsockname()[0]
    ip_s.close()

    return ip