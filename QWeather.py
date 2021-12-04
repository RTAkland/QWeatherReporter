#!/usr/bin/env python3
# -- coding:utf-8 --
# @Author: markushammered@gmail.com
# @Development Tool: PyCharm
# @Create Time: 2021/10/23
# @File Name: QWeather.py


import os
import sys
import json
import time
import pandas
import smtplib
import getpass
import requests
import argparse
import multiprocessing
import logging.handlers

from ruamel.yaml import YAML
from email.header import Header
from email.mime.text import MIMEText
from colorlog import ColoredFormatter
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart


class SendWeatherMail:
    def __init__(self):
        with open(CONFIG_NAME, 'r', encoding='utf-8') as config_f:
            self.config = YAML().load(config_f)
        with open('resource/type_warning.json', 'r', encoding='utf-8') as type_f:
            self.type_name = json.loads(type_f.read())

        self.location = self.config['request-settings']['location']  # 城市ID
        self.key = self.config['request-settings']['key']  # API密钥
        self.unit = self.config['request-settings']['unit']  # 度量单位
        self.lang = self.config['request-settings']['lang']  # 语言
        self.mode = self.config['request-settings']['mode']  # 发送模式 --仅作判断标识
        self.receiver = self.config['request-settings']['receiver']  # 接收者邮箱 --> 列表 [无论有几个人都必须是列表]
        self.sender = self.config['mail-settings']['sender']  # 发送者邮箱
        self.password = self.config['mail-settings']['password']  # 服务器登录密码
        self.server = self.config['mail-settings']['server']  # 邮箱服务器
        self.port = self.config['mail-settings']['port']  # 邮箱端口号
        self.icon_style = self.config['client-settings']['icon-style']  # 天气图标
        self.enableSSL = self.config['client-settings']  # 是否使用SSL连接到邮箱服务器
        self.city_name = self.config['only-view-settings']['city-name']  # 城市名称仅作邮件内容

        self.style_list = ['style1', 'style2', 'style3']

        # 如果配置文件内填错 默认选择第一套图标(style1)
        if self.icon_style not in self.style_list:
            self.icon_style = 'style1'

        self.dev_url = 'https://devapi.qweather.com/v7/weather/7d'  # 开发版本天气信息url
        self.free_url = 'https://devapi.qweather.com/v7/weather/3d'  # 免费版本天气信息url
        self.warning_url = 'https://devapi.qweather.com/v7/warning/now'  # 自然灾害预警信息url

        self.headers = {'Accept-Encoding': 'gzip, deflate'}  # 请求头

        self.params = {'location': self.location,
                       'key': self.key,
                       'unit': self.unit,
                       'lang': self.lang}  # GET方式请求参数

        self.message = MIMEMultipart('related')
        self.message['From'] = Header('QWeather')  # 发件人名称
        self.message['To'] = Header('All allowed User')  # 收件人显示名称
        self.msg_content = MIMEMultipart('alternative')  # 文字目录

        if self.enableSSL:
            self.smtp = smtplib.SMTP_SSL(self.server, self.port)  # 登录服务器 使用SSL连接
        else:
            self.smtp = smtplib.SMTP(self.server, self.port)  # 登录邮箱服务器 不使用SSL连接

    def dev_mode(self):
        """
        开发版本发送邮件
        [全七天] | date: 日期 (1-7)
        [全七天] | day_weather: 白天天气 (1-7)
        [全七天] | night_weather: 晚上天气 (1-7)
        [全七天] | temperature_max: 最高气温 (1-7)
        [全七天] | temperature_min: 最低气温 (1-7)
        [全七天] | icon_list: 白天和晚上的天气图标 (1-14)
        [第一天] | sunrise: 日出时间 (1)
        [第一天] | sunset: 日落时间 (1)
        [第一天] | humidity: 空气湿度(相对) (1)
        [第一天] | wind_speed: 风速 (1)
        [第一天] | wind_scale: 风级 (1)
        [第一天] | wind_dir: 风向 (1)
        [第一天] | ultraviolet_rays: 紫外线强度指数 (1)
        [第一天] | cloud: 云量(相对) (1)
        [第一天] | pressure: 气压 (1)
        [第一天] | vis: 能见度 (1)
        :return: None
        """
        r_day = session.get(self.dev_url, headers=self.headers, params=self.params)

        weather_day_text = r_day.json()  # 使用json加载数据
        logger.info(f'{language["request_result_weather"]}:{r_day}')

        # 1-7天数据
        day_1 = weather_day_text['daily'][0]
        day_2 = weather_day_text['daily'][1]
        day_3 = weather_day_text['daily'][2]
        day_4 = weather_day_text['daily'][3]
        day_5 = weather_day_text['daily'][4]
        day_6 = weather_day_text['daily'][5]
        day_7 = weather_day_text['daily'][6]

        date = [day_1['fxDate'][5:], day_2['fxDate'][5:], day_3['fxDate'][5:], day_4['fxDate'][5:], day_5['fxDate'][5:],
                day_6['fxDate'][5:],
                day_7['fxDate'][5:]]
        day_weather = [day_1['textDay'], day_2['textDay'], day_3['textDay'], day_4['textDay'], day_5['textDay'],
                       day_6['textDay'], day_7['textDay']]
        night_weather = [day_1['textNight'], day_2['textNight'], day_3['textNight'], day_4['textNight'],
                         day_5['textNight'], day_6['textNight'], day_7['textNight']]
        temperature_max = [day_1['tempMax'], day_2['tempMax'], day_3['tempMax'], day_4['tempMax'], day_5['tempMax'],
                           day_6['tempMax'], day_7['tempMax']]
        temperature_min = [day_1['tempMin'], day_2['tempMin'], day_3['tempMin'], day_4['tempMin'], day_5['tempMin'],
                           day_6['tempMin'], day_7['tempMin']]
        icon_list = [day_1['iconDay'], day_2['iconDay'], day_3['iconDay'], day_4['iconDay'], day_5['iconDay'],
                     day_6['iconDay'], day_7['iconDay'], day_1['iconNight'], day_2['iconNight'], day_3['iconNight'],
                     day_4['iconNight'], day_5['iconNight'], day_6['iconNight'], day_7['iconNight']]

        sunset = day_1['sunset']
        sunrise = day_1['sunrise']
        humidity = day_1['humidity']
        wind_speed = day_1['windSpeedDay']
        wind_scale = day_1['windScaleDay']
        wind_dir = day_1['windDirDay']
        ultraviolet_rays = day_1['uvIndex']
        cloud = day_1['cloud']
        pressure = day_1['pressure']
        vis = day_1['vis']

        # 邮件内容主体
        mail_html = f"""
        <p style="text-align: center">
            <i>
                <b>
                    {language['area']}:{self.city_name}
                    <br>
                    {language['sender']}:{self.sender}
                </b>
            </i>
        </p>
        <br />
        <table style="border: 0; text-align: center; margin:0 auto">
            <tr>
                <th>|&nbsp;{language['date']}&nbsp;&nbsp;</th>
                <th>|&nbsp;{language['weather']}&nbsp;&nbsp;</th>
                <th>|&nbsp;{language['lowestTemp']}&nbsp;&nbsp;</th>
                <th>|&nbsp;{language['highestTemp']}&nbsp;&nbsp;</th>
            </tr>
            <tr>
                <!--日期 天气 最低 最高/Date Weather LowestTemp HighestTemp-->
                <td>{language['today']}</td>
                <td>{day_weather[0]}<img src="cid:img1" width="20" alt="">/{night_weather[0]}<img src="cid:img2" 
                width="20" alt=""></td> <td>{temperature_min[0]}℃</td> 
                <td>{temperature_max[0]}℃</td>
            </tr>
            <tr>
                <td>{date[1]}</td>
                <td>{day_weather[1]}<img src="cid:img3" width="20" alt="">/{night_weather[1]}<img src="cid:img4" 
                width="20" alt=""></td> <td>{temperature_min[1]}℃</td> 
                <td>{temperature_max[1]}℃</td>
            </tr>
                <tr>
                <td>{date[2]}</td>
                <td>{day_weather[2]}<img src="cid:img5" width="20" alt="">/{night_weather[2]}<img src="cid:img6" 
                width="20" alt=""></td> <td>{temperature_min[2]}℃</td> 
                <td>{temperature_max[2]}℃</td>
            </tr>
                <tr>
                <td>{date[3]}</td>
                <td>{day_weather[3]}<img src="cid:img7" width="20" alt="">/{night_weather[3]}<img src="cid:img8" 
                width="20" alt=""></td> <td>{temperature_min[3]}℃</td> 
                <td>{temperature_max[3]}℃</td>
            </tr>
                <tr>
                <td>{date[4]}</td>
                <td>{day_weather[4]}<img src="cid:img9" width="20" alt="">/{night_weather[4]}<img src="cid:img10" 
                width="20" alt=""></td> <td>{temperature_min[4]}℃</td> 
                <td>{temperature_max[4]}℃</td>
            </tr>
                <tr>
                <td>{date[5]}</td>
                <td>{day_weather[5]}<img src="cid:img11" width="20" alt="">/{night_weather[5]}<img src="cid:img12" 
                width="20" alt=""></td> <td>{temperature_min[5]}℃</td> 
                <td>{temperature_max[5]}℃</td>
            </tr>
                <tr>
                <td>{date[6]}</td>
                <td>{day_weather[6]}<img src="cid:img13" width="20" alt="">/{night_weather[6]}<img src="cid:img14" 
                width="20" alt=""></td> <td>{temperature_min[6]}℃</td> 
                <td>{temperature_max[6]}℃</td>
            </tr>
        </table>
        <table style="border: 0;text-align: center; margin:0 auto">
            <tr>
                <th>&nbsp;</th>
            </tr>
            <tr>
                <th>{language['wind_info']}</th>
                <th>{language['humidity']}</th>
                <th>{language['uv_info']}</th>
            </tr>
            <tr>
                <td>{wind_speed}m/s&nbsp; {wind_scale}&nbsp; {wind_dir}&nbsp;</td>
                <td>{humidity}%&nbsp;</td>
                <td>{ultraviolet_rays}&nbsp;</td>
            </tr>
            <tr>
                <th>&nbsp;</th>
            </tr>
            <tr>
                <th>{language['vis']}</th>
                <th>{language['pressure']}</th>
                <th>{language['cloud']}</th>
            </tr>
            <tr>
                <td>{vis}km&nbsp;</td>
                <td>{pressure}hPa&nbsp;</td>
                <td>{cloud}%&nbsp;</td>
            </tr>
        </table>
        <table style="border: 0;text-align: center; margin:0 auto">
            <tr>
                <th>&nbsp;</th>
            </tr>
            <tr>
                <td><img src="cid:sunrise" alt="Sunrise" width="30"></td>
                <td>&nbsp;</td>
                <td><img src="cid:sunset" alt="Sunset" width="30"></td>
            </tr>
            <tr>
                <td>&nbsp;{sunrise}&nbsp;</td>
                <td>---------------</td>
                <td>&nbsp;{sunset}&nbsp;</td>
            </tr>
        </table>
        <div style="text-align: center;" id="About">
            <br />
            <br />
            <br />
            <i>
                <b>
                    <a href="https://dev.qweather.com/" style="color: black" target="_blank">QWeather</a>
                    <a style="color: black">&nbsp;·&nbsp;</a>
                    <a href="https://github.com/MarkusJoe/QWeather" style="color: black" target="_blank">Github Repo</a>
                </b>
            </i>
        </div>"""
        self.message['Subject'] = language['subject_7']  # 邮件标题
        self.message.attach(MIMEText(mail_html, 'html', 'utf-8'))

        # 循环将图片attach到html里
        image_count = 1
        for image_resource in icon_list:
            with open(f'./resource/{self.icon_style}/{image_resource}.png', 'rb') as fp:
                MyImage = MIMEImage(fp.read())
                MyImage.add_header('Content-ID', f'img{image_count}')
                self.message.attach(MyImage)
                image_count += 1

        with open('resource/basic-resources/sunrise.png', 'rb') as sr_f:
            sunrise_img = MIMEImage(sr_f.read())
            sunrise_img.add_header('Content-ID', 'sunrise')
            self.message.attach(sunrise_img)
        with open('resource/basic-resources/sunset.png', 'rb') as ss_f:
            sunset_img = MIMEImage(ss_f.read())
            sunset_img.add_header('Content-ID', 'sunset')
            self.message.attach(sunset_img)

        try:
            self.smtp.login(self.sender, self.password)  # 登录
            self.smtp.sendmail(self.sender, self.receiver, self.message.as_string())  # 发送
        except smtplib.SMTPException as e:
            logger.critical(f'{language["mail_error"]}:', e)
            sys.exit(1)

    def free_mode(self):
        """
        免费版本发送邮件
        :return:
        """
        f_request = session.get(self.free_url, headers=self.headers, params=self.params)
        f_weather = f_request.json()

        logger.info(f'{language["request_result_weather"]}:{f_request}')

        day_1 = f_weather['daily'][0]
        day_2 = f_weather['daily'][1]
        day_3 = f_weather['daily'][2]

        date = [day_1['fxDate'][5:], day_2['fxDate'][5:], day_2['fxDate'][5:]]
        day_weather = [day_1['textDay'], day_2['textDay'], day_2['textDay']]
        night_weather = [day_1['textNight'], day_2['textNight'], day_2['textNight']]
        temperature_max = [day_1['tempMax'], day_2['tempMax'], day_3['tempMax']]
        temperature_min = [day_1['tempMin'], day_2['tempMin'], day_2['tempMin']]
        icon_list = [day_1['iconDay'], day_1['iconDay'], day_3['iconDay'], day_1['iconNight'], day_2['iconNight'],
                     day_3['iconNight']]

        sunset = day_1['sunset']
        sunrise = day_1['sunrise']
        humidity = day_1['humidity']
        wind_speed = day_1['windSpeedDay']
        wind_scale = day_1['windScaleDay']
        wind_dir = day_1['windDirDay']
        ultraviolet_rays = day_1['uvIndex']
        cloud = day_1['cloud']
        pressure = day_1['pressure']
        vis = day_1['vis']

        mail_html = f"""
        <p style="text-align: center">
            <i>
                <b>
                    {language['area']}:{self.city_name}
                    <br>
                    {language['sender']}:{self.sender}
                </b>
            </i>
        </p>
        <br />
        <table style="border: 0; text-align: center; margin:0 auto">
            <tr>
                <th>|&nbsp;{language['date']}&nbsp;&nbsp;</th>
                <th>|&nbsp;{language['weather']}&nbsp;&nbsp;</th>
                <th>|&nbsp;{language['lowestTemp']}&nbsp;&nbsp;</th>
                <th>|&nbsp;{language['highestTemp']}&nbsp;&nbsp;</th>
            </tr>
            <tr>
                <!--日期 天气 最低 最高/Date Weather LowestTemp HighestTemp-->
                <td>{language['today']}</td>
                <td>{day_weather[0]}<img src="cid:img1" width="20" alt="">/{night_weather[0]}<img src="cid:img2" 
                width="20" alt=""></td> <td>{temperature_min[0]}℃</td> 
                <td>{temperature_max[0]}℃</td>
            </tr>
            <tr>
                <td>{date[1]}</td>
                <td>{day_weather[1]}<img src="cid:img3" width="20" alt="">/{night_weather[1]}<img src="cid:img4" 
                width="20" alt=""></td> <td>{temperature_min[1]}℃</td> 
                <td>{temperature_max[1]}℃</td>
            </tr>
                <tr>
                <td>{date[2]}</td>
                <td>{day_weather[2]}<img src="cid:img5" width="20" alt="">/{night_weather[2]}<img src="cid:img6" 
                width="20" alt=""></td> <td>{temperature_min[2]}℃</td> 
                <td>{temperature_max[2]}℃</td>
            </tr>
        </table>
        <table style="border: 0;text-align: center; margin:0 auto">
            <tr>
                <th>&nbsp;</th>
            </tr>
            <tr>
                <th>{language['wind_info']}</th>
                <th>{language['humidity']}</th>
                <th>{language['uv_info']}</th>
            </tr>
            <tr>
                <td>{wind_speed}m/s&nbsp; {wind_scale}&nbsp; {wind_dir}&nbsp;</td>
                <td>{humidity}%&nbsp;</td>
                <td>{ultraviolet_rays}&nbsp;</td>
            </tr>
            <tr>
                <th>&nbsp;</th>
            </tr>
            <tr>
                <th>{language['vis']}</th>
                <th>{language['pressure']}</th>
                <th>{language['cloud']}</th>
            </tr>
            <tr>
                <td>{vis}km&nbsp;</td>
                <td>{pressure}hPa&nbsp;</td>
                <td>{cloud}%&nbsp;</td>
            </tr>
        </table>
        <table style="border: 0;text-align: center; margin:0 auto">
            <tr>
                <th>&nbsp;</th>
            </tr>
            <tr>
                <td><img src="cid:sunrise" alt="Sunrise" width="30"></td>
                <td>&nbsp;</td>
                <td><img src="cid:sunset" alt="Sunset" width="30"></td>
            </tr>
            <tr>
                <td>&nbsp;{sunrise}&nbsp;</td>
                <td>---------------</td>
                <td>&nbsp;{sunset}&nbsp;</td>
            </tr>
        </table>
        <div style="text-align: center;" id="About">
            <br />
            <br />
            <br />
            <i>
                <b>
                    <a href="https://dev.qweather.com/" style="color: black" target="_blank">QWeather</a>
                    <a style="color: black">&nbsp;·&nbsp;</a>
                    <a href="https://github.com/MarkusJoe/QWeather" style="color: black" target="_blank">Github Repo</a>
                </b>
            </i>
        </div>"""
        self.message['Subject'] = language['subject_3']
        self.message.attach(MIMEText(mail_html, 'html', 'utf-8'))

        image_count = 1
        for image_source_free in icon_list:
            with open(f'./resource/{self.icon_style}/{image_source_free}.png', 'rb') as file:
                MyImage = MIMEImage(file.read())
            MyImage.add_header('Content-ID', f'img{image_count}')
            self.message.attach(MyImage)
            image_count += 1

        with open('resource/basic-resources/sunrise.png', 'rb') as sr_f:
            sunrise_img = MIMEImage(sr_f.read())
            sunrise_img.add_header('Content-ID', 'sunrise')
            self.message.attach(sunrise_img)
        with open('resource/basic-resources/sunset.png', 'rb') as ss_f:
            sunset_img = MIMEImage(ss_f.read())
            sunset_img.add_header('Content-ID', 'sunset')
            self.message.attach(sunset_img)

        try:
            self.smtp.login(self.sender, self.password)
            self.smtp.sendmail(self.sender, self.receiver, self.message.as_string())
        except smtplib.SMTPException as e:
            logger.critical(f'{language["mail_error"]}:', e)
            sys.exit(1)

    def warning_send_mail(self):
        """
        发送自然灾害预警信息
        releaseTime: 更新时间(并不是获取数据的时间 而是API更新数据的时间)
        title: 标题
        startTime: 开始时间
        endTime: 结束时间
        status: 状态
        level: 等级
        type: 类型
        text: 详细描述
        获取自然灾害并判断灾害信息是否为空
        如果空则跳过
        如果不为空则单独发送一封邮件
        :return:
        """
        r = session.get(self.warning_url, headers=self.headers, params=self.params)
        data = r.json()

        logger.info(f'{language["request_result_warning"]}:{data["code"]}')
        if data['warning']:
            public_time = data['warning'][0]['pubTime']
            title = data['warning'][0]['title']
            start_time = data['warning'][0]['startTime']
            end_time = data['warning'][0]['endTime']
            if not start_time:
                start_time = None
            elif not end_time:
                end_time = None
            warning_status = data['warning'][0]['status']
            if warning_status == 'update':
                warning_status = {language["new_warning"]}
                logger.info(f'{language["new_warning"]}')
            elif warning_status == 'active':
                warning_status = language["warning_updated"]
                logger.info(f'{language["warning_updated"]}')
            elif warning_status == 'cancel':
                logger.info(f'{language["warning_canceled"]}')

            level = data['warning'][0]['level']
            type_ = data['warning'][0]['type']
            type_ = self.type_name[type_]  # 将数字type转换为文字
            text = data['warning'][0]['text']
            self.message['Subject'] = language['subject_war']
            self.message['Subject'] = f'{title}'
            mail_html = f"""
            <!DOCTYPE html>
            <html lang="zh">
            <head>
                <meta charset="UTF-8">
                <title>Warning</title>
            </head>
            <body>
            <div style="text-align: center;color: black;">
                <h2>{title}</h2>
                <h3>{language['release_time']}:{public_time[:10]} {level}{language['early_warning']}</h3>
                <p>
                    {language['warning_status']}:{warning_status} {language['warning_type']}:{type_} {language['warning_duration']}:{start_time[:10]}-{end_time[:10]}
                    <br />
                    {text}
                </p>
            </div>
            <div style="text-align: center;" id="About">
                <br />
                <br />
                <br />
                <i>
                    <b>
                        <a href="https://dev.qweather.com/" style="color: black" target="_blank">QWeather</a>
                        <a style="color: black">&nbsp;·&nbsp;</a>
                        <a href="https://github.com/MarkusJoe/QWeather" style="color: black" target="_blank">Github Repo</a>
                    </b>
                </i>
            </div>
            </body>
            </html>
            """
            self.msg_content.attach(MIMEText(mail_html, 'html', 'utf-8'))
            self.message.attach(self.msg_content)
            try:
                if warning_status != 'cancel':
                    self.smtp.login(self.sender, self.password)
                    self.smtp.sendmail(self.sender, self.receiver, self.message.as_string())
            except smtplib.SMTPException as e:
                logger.error(f'{language["mail_error"]}:', e)
                sys.exit(1)


def loop_check(mode: str, time_list: list):
    """
    循环检测时间如果本地时间等于配置文件内填写的时间则发送一封天气信息的邮件
    :return:
    """
    match mode:
        case 'dev':
            while True:
                local_time = time.strftime("%H:%M", time.localtime())
                time.sleep(1)
                if local_time in time_list:
                    SendWeatherMail().dev_mode()
                    logger.info(f'{language["mail_succeed"]}')
                    logger.info(f'{language["wait_seconds"]}')
                    time.sleep(61)
        case 'free':
            while True:
                local_time = time.strftime("%H:%M", time.localtime())
                time.sleep(1)
                if local_time in time_list:
                    SendWeatherMail().free_mode()
                    logger.info(f'{language["mail_succeed"]}')
                    logger.info(f'{language["wait_seconds"]}')
                    time.sleep(61)


def check_config():
    """
    检查各项配置是否填写完成
    :return:
    """
    for mail in config['mail-settings'].values():
        if mail is None:
            logger.critical(f'"mail-settings"{language["config_not_filled"]}')
            sys.exit(1)
    for request in config['request-settings'].values():
        if request is None:
            logger.critical(f'"request-settings"{language["config_not_filled"]}')
            sys.exit(1)
    for other in config['client-settings'].values():
        if other is None:
            logger.critical(f'"client-settings"{language["config_not_filled"]}')
            sys.exit(1)


def read_excel(kw: str):
    """
    读取xlsx城市ID文件并返回搜索到的结果
    :param kw: 用于搜索的关键字
    :return: city_list
    """
    index_count = 0
    city_list = []
    logger.info(f'[Search]{language["reading_the_file"]}')
    df = pandas.read_excel(f'./resource/{LOCATION_ID_FILE_NAME}')
    pandas.set_option('max_rows', None)  # 读取xlsx文件不折叠
    data_records = df.to_dict(orient='split')
    for i in data_records['data']:
        if kw in str(i):
            logger.info(f'{index_count}|{i[0]}-{i[2]}-{i[4]}-{i[6]}')
            city = [index_count, i[0], i[1], i[2], i[3], i[4], i[5], i[6], i[7], i[8], i[9]]
            index_count += 1
            city_list.append(city)
    return city_list


def modify_config(mode: bool = False):
    """
    修改配置文件 -> 检测配置文件内的location项是否填写
    填写 -> 跳过
    未填写 -> 触发
    (如果不小心在location项内随便输入了什么会导致误判)
    :param mode: 触发修改模式的条件
    :return: Nothing
    """

    if not _LOCATION or not mode:  # 如果配置中location未填写或status未False则触发条件
        logger.info(f'[Modify]{language["fill_the_config"]}')
        logger.info(f'[Modify]{language["input_a_city_name"]}')
        while True:
            time.sleep(0.3)
            city_name = input('-->')
            match city_name:
                case 'q':
                    logger.info(f'[Modify]User quit.')
                    sys.exit(0)
                case '':
                    logger.critical(f'[Modify]{language["null_value"]}')
                    continue
                case _:
                    break
        searched_city = read_excel(city_name)
        logger.info(f'[Modify]{language["user_input"]}:[{city_name}]')
        logger.info(f'[Modify]{language["select_a_index"]}')
        if not searched_city:
            logger.error(f'[Modify]{language["no_result"]}')
            sys.exit(1)
        time.sleep(0.3)
        while True:
            try:
                time.sleep(0.3)
                user_input = input('-->')
                if user_input == 'q':
                    logger.info('[Quit]User quit')
                    sys.exit(1)
                index = searched_city[int(user_input)]
                with open(CONFIG_NAME, 'r', encoding='utf-8') as of:
                    data = YAML().load(of)
                    data['request-settings']['location'] = index[1]
                    data['only-view-settings']['city-name'] = f'{index[3]}-{index[7]}-{index[7]}'
                    data['only-view-settings']['time'] = time.strftime("%a %b %d %Y %H:%M:%S", time.localtime())
                    data['only-view-settings']['user'] = getpass.getuser()
                with open(CONFIG_NAME, 'w', encoding='utf-8') as wf:
                    YAML().dump(data, wf)
                logger.info(f'[Write]{language["write_successfully"]}:{CONFIG_NAME}')
                break
            except (IndexError, ValueError) as e:
                logger.info(e)
                logger.error(f'[Write]{language["input_type_error"]}')
                continue
            finally:
                logger.info('[Done]Program has done.')
                sys.exit(0)


if __name__ == '__main__':
    CONFIG_NAME = 'config.yml'  # 配置文件名称
    LOCATION_ID_FILE_NAME = 'china_city_list.xlsx'  # 城市id文件必须为xlsx文件

    # logs为空文件夹git上传时会自动忽略此文件夹， 故添加自动创建文件夹
    if not os.path.isdir('./logs'):
        os.mkdir('./logs')

    date_format = '%H:%M:%S'
    info_format_console = '%(log_color)s[%(asctime)s] |%(levelname)-8s |%(lineno)-3s |%(message)s'
    info_format_file = '[%(asctime)s] |%(levelname)-8s |%(lineno)-3s |%(funcName)s |%(pathname)s |%(message)s'
    formatter = ColoredFormatter(fmt=info_format_console,
                                 datefmt=date_format,
                                 reset=True,
                                 log_colors={
                                     'DEBUG': 'light_purple',
                                     'INFO': 'light_cyan',
                                     'WARNING': 'yellow',
                                     'ERROR': 'red',
                                     'CRITICAL': 'red,bold_red'})
    formatter_file = logging.Formatter(fmt=info_format_file,
                                       datefmt=date_format)

    logger = logging.getLogger('MainLogger')
    logger.setLevel(logging.DEBUG)
    ConsoleLogger = logging.StreamHandler()  # 输出到终端
    ConsoleLogger.setFormatter(formatter)
    log_name = time.strftime('%Y-%m-%d#%H')  # 一小时内使用的日志文件都是同一个
    FileLogger = logging.handlers.RotatingFileHandler(filename=f'./logs/{log_name}.log',
                                                      maxBytes=10240,
                                                      backupCount=5)  # 每个日志文件最大10240字节(10Kb)
    FileLogger.setFormatter(formatter_file)
    logger.addHandler(ConsoleLogger)
    logger.addHandler(FileLogger)

    # 使用本地网络进行请求
    session = requests.Session()
    session.trust_env = False

    # 获取语言配置
    with open(CONFIG_NAME, 'r', encoding='utf-8') as lang:
        config = YAML().load(lang.read())
        language_sel = config['client-settings']['language']
        if language_sel not in ['zh_cn', 'en_us']:
            language_sel = 'zh_cn'

    # 打开语言json文件
    with open(f'./resource/lang/{language_sel}.json', 'r', encoding='utf-8') as lang_f:
        language = json.loads(lang_f.read())

    _TIMES = config['client-settings']['send-times']
    _MODE = config['request-settings']['mode']
    _LOCATION = config['request-settings']['location']

    modify_config(True)

    # 获取参数
    parser = argparse.ArgumentParser()
    arg_keywords = ['free', 'dev', 'warning', 'modify']
    parser.add_argument('-t',
                        '--test',
                        help='Some operations for test.',
                        choices=arg_keywords)
    startup_arg = parser.parse_args().test
    # Python3.10 更新的match-case 语法
    match startup_arg:
        case 'free':
            SendWeatherMail().free_mode()
            logger.debug(f'{language["debug_done"]}')
            sys.exit(0)
        case 'dev':
            SendWeatherMail().dev_mode()
            logger.debug(f'{language["debug_done"]}')
            sys.exit(0)
        case 'warning':
            SendWeatherMail().warning_send_mail()
            logger.debug(f'{language["debug_done"]}')
            sys.exit(0)
        case 'modify':
            modify_config()
            logger.info(f'{language["debug_done"]}')
        case _:
            pass

    # 检查配置文件是否填写完成
    check_config()

    # 输出声明
    logger.info(f'{language["statement_1"]}')
    logger.info(f'{language["statement_2"]}')
    logger.info(f'{language["statement_3"]}')
    logger.info(f'{language["statement_4"]}')
    logger.info(f'{language["current_profile"]}')

    #  另开一个进程与主进程同时运行 --> 运行loopCheck --> 循环检查本地时间是否与配置内时间相符
    multiprocessing.Process(target=loop_check, args=(_MODE, _TIMES,)).run()

    # 循环检测时间 --> 每10分钟检查一次, 如果有则发送如果无则直接跳过
    loop_timer = 0
    while True:
        time.sleep(1)
        loop_timer += 1
        if loop_timer == 600:
            SendWeatherMail().warning_send_mail()
            loop_timer = 0
