#!/usr/bin/env python3
# -- coding:utf-8 --
# @Author: markushammered@gmail.com
# @Development Tool: PyCharm
# @Create Time: 2021/12/15
# @File Name: settings.py

import sys
import time
import getpass
from core.logger import Logger
from core.language import Language
from core.read_excel import read_excel
from ruamel.yaml import YAML


def change_settings(mode: bool = False, _flag: bool = False):
    """

    :param _flag:
    :param mode:
    :return:
    """
    language = Language()

    if not _flag or not mode:  # 如果配置中location未填写或status未False则触发条件
        Logger.info(f'[Modify]{language["fill_the_config"]}')
        Logger.info(f'[Modify]{language["input_a_city_name"]}')
        while True:
            time.sleep(0.3)
            city_name = input('-->')
            match city_name:
                case 'q':
                    Logger.info(f'[Modify]User quit.')
                    sys.exit(0)
                case '':
                    Logger.critical(f'[Modify]{language["null_value"]}')
                    continue
                case _:
                    break
        searched_city = read_excel(city_name)
        Logger.info(f'[Modify]{language["user_input"]}:[{city_name}]')
        Logger.info(f'[Modify]{language["select_a_index"]}')
        if not searched_city:
            Logger.error(f'[Modify]{language["no_result"]}')
            sys.exit(1)
        time.sleep(0.3)
        while True:
            try:
                time.sleep(0.3)
                user_input = input('-->')
                if user_input == 'q':
                    Logger.info('[Quit]User quit')
                    sys.exit(1)
                index = searched_city[int(user_input)]
                with open('./config.yml', 'r', encoding='utf-8') as of:
                    data = YAML().load(of)
                    data['request-settings']['location'] = index[1]
                    data['only-view-settings']['city-name'] = f'{index[3]}-{index[7]}-{index[7]}'
                    data['only-view-settings']['time'] = time.strftime("%a %b %d %Y %H:%M:%S", time.localtime())
                    data['only-view-settings']['user'] = getpass.getuser()
                with open('./config.yml', 'w', encoding='utf-8') as wf:
                    YAML().dump(data, wf)
                Logger.info(f'[Write]{language["write_successfully"]}:config.yml')
                break
            except (IndexError, ValueError) as e:
                Logger.info(e)
                Logger.error(f'[Write]{language["input_type_error"]}')
                continue
            finally:
                Logger.info('[Done]Program has done.')
                sys.exit(0)
