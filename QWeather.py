#!/usr/bin/env python
# -- coding:utf-8 --
# @Author: markushammered@gmail.com
# @Development Tool: PyCharm
# @Create Time: 2021/10/23
# @File Name: QWeather.py


import sys
import json
import time
import smtplib
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
        with open(my_config_file, 'r', encoding='utf-8') as config_f:
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
        self.SSL = self.config['client-settings']  # 是否使用SSL连接到邮箱服务器
        self.city_name = self.config['only-view-settings']['city-name']  # 城市名称仅作邮件内容

        self.style_list = ['style1', 'style2', 'style3']

        # 如果配置文件内填错或不填 默认选择第一套图标(style1)
        if self.icon_style not in self.style_list:
            self.icon_style = 'style1'

        self.Dev_Link = f'https://devapi.qweather.com/v7/weather/7d?location=' \
                        f'{self.location}&key={self.key}&unit={self.unit}&lang={self.lang}'
        self.Free_Link = f'https://devapi.qweather.com/v7/weather/3d?location=' \
                         f'{self.location}&key={self.key}&unit={self.unit}&lang={self.lang}'

        self.message = MIMEMultipart('related')
        self.message['From'] = Header('HeWeatherReporter')  # 发件人名称
        self.message['To'] = Header('All allowed User')  # 收件人显示名称
        self.msg_content = MIMEMultipart('alternative')  # 文字目录

        if self.SSL:
            self.smtp = smtplib.SMTP_SSL(self.server, self.port)  # 登录服务器 使用SSL连接
        else:
            self.smtp = smtplib.SMTP(self.server, self.port)  # 登录邮箱服务器 不使用SSL连接

    def Dev_mode(self):
        """
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
        r_day = session.get(self.Dev_Link, headers={'Accept-Encoding': 'gzip'})

        weather_day_text = json.loads(r_day.text)  # 使用json加载数据
        logger.info(f'{language["request_result_weather"]}:{r_day}')

        # 1-7天数据
        day_1 = weather_day_text['daily'][0]
        day_2 = weather_day_text['daily'][1]
        day_3 = weather_day_text['daily'][2]
        day_4 = weather_day_text['daily'][3]
        day_5 = weather_day_text['daily'][4]
        day_6 = weather_day_text['daily'][5]
        day_7 = weather_day_text['daily'][6]

        date = [day_1['fxDate'][2:], day_2['fxDate'][2:], day_3['fxDate'][2:], day_4['fxDate'][2:], day_5['fxDate'][2:],
                day_6['fxDate'][2:],
                day_7['fxDate'][2:]]
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

        # 邮件内容主体 -> 为适应邮件html的渲染机制 -> 不使用<head>;<body>;全局变量 等
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
                <td>{date[0]}</td>
                <td>{day_weather[0]}<img src="cid:img1" width="20" alt="">/{night_weather[0]}<img src="cid:img2" width="20" alt=""></td>
                <td>{temperature_min[0]}℃</td>
                <td>{temperature_max[0]}℃</td>
            </tr>
            <tr>
                <td>{date[1]}</td>
                <td>{day_weather[1]}<img src="cid:img3" width="20" alt="">/{night_weather[1]}<img src="cid:img4" width="20" alt=""></td>
                <td>{temperature_min[1]}℃</td>
                <td>{temperature_max[1]}℃</td>
            </tr>
                <tr>
                <td>{date[2]}</td>
                <td>{day_weather[2]}<img src="cid:img5" width="20" alt="">/{night_weather[2]}<img src="cid:img6" width="20" alt=""></td>
                <td>{temperature_min[2]}℃</td>
                <td>{temperature_max[2]}℃</td>
            </tr>
                <tr>
                <td>{date[3]}</td>
                <td>{day_weather[3]}<img src="cid:img7" width="20" alt="">/{night_weather[3]}<img src="cid:img8" width="20" alt=""></td>
                <td>{temperature_min[3]}℃</td>
                <td>{temperature_max[3]}℃</td>
            </tr>
                <tr>
                <td>{date[4]}</td>
                <td>{day_weather[4]}<img src="cid:img9" width="20" alt="">/{night_weather[4]}<img src="cid:img10" width="20" alt=""></td>
                <td>{temperature_min[4]}℃</td>
                <td>{temperature_max[4]}℃</td>
            </tr>
                <tr>
                <td>{date[5]}</td>
                <td>{day_weather[5]}<img src="cid:img11" width="20" alt="">/{night_weather[5]}<img src="cid:img12" width="20" alt=""></td>
                <td>{temperature_min[5]}℃</td>
                <td>{temperature_max[5]}℃</td>
            </tr>
                <tr>
                <td>{date[6]}</td>
                <td>{day_weather[6]}<img src="cid:img13" width="20" alt="">/{night_weather[6]}<img src="cid:img14" width="20" alt=""></td>
                <td>{temperature_min[6]}℃</td>
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
                    <a href="https://github.com/MarkusJoe/HeWeatherReporter" style="color: black" target="_blank">Github Repo</a>
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

        with open('./resource/extra-icon/sunrise.png', 'rb') as sr_f:
            sunrise_img = MIMEImage(sr_f.read())
            sunrise_img.add_header('Content-ID', 'sunrise')
            self.message.attach(sunrise_img)
        with open('./resource/extra-icon/sunset.png', 'rb') as ss_f:
            sunset_img = MIMEImage(ss_f.read())
            sunset_img.add_header('Content-ID', 'sunset')
            self.message.attach(sunset_img)

        try:
            self.smtp.login(self.sender, self.password)  # 登录
            self.smtp.sendmail(self.sender, self.receiver, self.message.as_string())  # 发送
        except smtplib.SMTPException as e:
            logger.critical(f'{language["mail_error"]}:', e)
            sys.exit(1)

    # 免费版本
    def Free_mode(self):
        f_request = session.get(self.Free_Link, headers={'Accept-Encoding': 'gzip'})
        f_weather = json.loads(f_request.text)

        logger.info(f'{language["request_result_weather"]}:{f_request}')

        day_1 = f_weather['daily'][0]
        day_2 = f_weather['daily'][1]
        day_3 = f_weather['daily'][2]

        date = [day_1['fxDate'], day_2['fxDate'], day_2['fxDate']]
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
                <td>{date[0]}</td>
                <td>{day_weather[0]}<img src="cid:img1" width="20" alt="">/{night_weather[0]}<img src="cid:img2" width="20" alt=""></td>
                <td>{temperature_min[0]}℃</td>
                <td>{temperature_max[0]}℃</td>
            </tr>
            <tr>
                <td>{date[1]}</td>
                <td>{day_weather[1]}<img src="cid:img3" width="20" alt="">/{night_weather[1]}<img src="cid:img4" width="20" alt=""></td>
                <td>{temperature_min[1]}℃</td>
                <td>{temperature_max[1]}℃</td>
            </tr>
                <tr>
                <td>{date[2]}</td>
                <td>{day_weather[2]}<img src="cid:img5" width="20" alt="">/{night_weather[2]}<img src="cid:img6" width="20" alt=""></td>
                <td>{temperature_min[2]}℃</td>
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
                    <a href="https://github.com/MarkusJoe/HeWeatherReporter" style="color: black" target="_blank">Github Repo</a>
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

            with open('./resource/extra-icon/sunrise.png', 'rb') as sr_f:
                sunrise_img = MIMEImage(sr_f.read())
                sunrise_img.add_header('Content-ID', 'sunrise')
                self.message.attach(sunrise_img)
            with open('./resource/extra-icon/sunset.png', 'rb') as ss_f:
                sunset_img = MIMEImage(ss_f.read())
                sunset_img.add_header('Content-ID', 'sunset')
                self.message.attach(sunset_img)

        try:
            self.smtp.login(self.sender, self.password)
            self.smtp.sendmail(self.sender, self.receiver, self.message.as_string())
        except smtplib.SMTPException as e:
            logger.critical(f'{language["mail_error"]}:', e)
            sys.exit(1)

    # 获取自然灾害
    def warning_send_mail(self):
        """

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
        API_url = f'https://devapi.qweather.com/v7/warning/now?location={self.location}&key={self.key}'
        r = session.get(API_url, headers={'Accept-Encoding': 'gzip'}).text
        data = json.loads(r)

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
            status = data['warning'][0]['status']
            if status == 'update':
                status = {language["new_warning"]}
                logger.info(f'{language["new_warning"]}')
            elif status == 'active':
                status = language["warning_updated"]
                logger.info(f'{language["warning_updated"]}')
            elif status == 'cancel':
                logger.info(f'{language["warning_canceled"]}')

            level = data['warning'][0]['level']
            type_ = data['warning'][0]['type']
            type_ = self.type_name[type_]
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
                    {language['warning_status']}:{status} {language['warning_type']}:{type_} {language['warning_duration']}:{start_time[:10]}-{end_time[:10]}
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
                        <a href="https://github.com/MarkusJoe/HeWeatherReporter" style="color: black" target="_blank">Github Repo</a>
                    </b>
                </i>
            </div>
            </body>
            </html>
            """
            self.msg_content.attach(MIMEText(mail_html, 'html', 'utf-8'))
            self.message.attach(self.msg_content)
            try:
                if status != 'cancel':
                    self.smtp.login(self.sender, self.password)
                    self.smtp.sendmail(self.sender, self.receiver, self.message.as_string())
            except smtplib.SMTPException as e:
                logger.error(f'{language["mail_error"]}:', e)
                sys.exit(1)


def loopCheck(mode: str, time_list: list):
    """
    循环检测时间如果本地时间等于配置文件内填写的时间则发送一封天气信息的邮件
    :return:
    """
    if mode == 'dev':
        while True:
            local_time = time.strftime("%H:%M", time.localtime())
            logger_file.info("There's no error. Program runs normally...")
            time.sleep(1)
            if local_time in time_list:
                SendWeatherMail().Dev_mode()
                logger.info(f'{language["mail_succeed"]}')
                logger.info(f'{language["wait_seconds"]}')
                time.sleep(61)
    elif mode == 'free':
        while True:
            local_time = time.strftime("%H:%M", time.localtime())
            logger_file.info("There's no error. Program runs normally...")
            time.sleep(1)
            if local_time in time_list:
                SendWeatherMail().Free_mode()
                logger.info(f'{language["mail_succeed"]}')
                logger.info(f'{language["wait_seconds"]}')
                time.sleep(61)


def checkConfig():
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


if __name__ == '__main__':
    my_config_file = 'config_owner.yml'

    formatter = ColoredFormatter("%(log_color)s[%(asctime)s] |%(levelname)-8s |%(lineno)-3s |%(message)s",
                                 datefmt='%H:%M:%S',
                                 reset=True,
                                 log_colors={
                                     'DEBUG': 'light_purple',
                                     'INFO': 'light_cyan',
                                     'WARNING': 'yellow',
                                     'ERROR': 'red',
                                     'CRITICAL': 'red,bold_red',
                                 })
    formatter_file = logging.Formatter(fmt='[%(asctime)s] |%(levelname)-8s |%(lineno)-3s |%(funcName)s |%(pathname)s |%(message)s', datefmt='%H:%M:%S')
    logger = logging.getLogger('MainLogger')
    logger_file = logging.getLogger('FileLogger')
    logger.setLevel(logging.DEBUG)
    logger_file.setLevel(logging.DEBUG)
    ConsoleLogger = logging.StreamHandler()
    ConsoleLogger.setFormatter(formatter)
    FileLogger = logging.handlers.RotatingFileHandler(filename=f'./logs/latest.log', maxBytes=102400, backupCount=5)
    FileLogger.setFormatter(formatter_file)
    logger.addHandler(ConsoleLogger)
    logger_file.addHandler(FileLogger)

    # 获取语言配置
    with open(my_config_file, 'r', encoding='utf-8') as lang:
        config = YAML().load(lang.read())
        language_sel = config['client-settings']['language']
        if language_sel not in ['zh_cn', 'en_us']:
            language_sel = 'zh_cn'

    # 打开语言json文件
    with open(f'./resource/lang/{language_sel}.json', 'r', encoding='utf-8') as lang_f:
        language = json.loads(lang_f.read())

    # 检查配置文件是否填写完成
    checkConfig()

    logger.info(f'{language["statement_1"]}')
    logger.info(f'{language["statement_2"]}')
    logger.info(f'{language["statement_3"]}')
    logger.info(f'{language["statement_4"]}\n')

    # 使用本地网络进行请求. 这都得益于Python urllib3的神奇"特性".
    session = requests.Session()
    session.trust_env = False

    # 获取参数
    parser = argparse.ArgumentParser()
    parser.add_argument('-t',
                        '--test',
                        help='Some operations for test.',
                        choices=['free',
                                 'dev',
                                 'warning']
                        )
    arg_test = parser.parse_args().test
    if arg_test:
        if arg_test == 'dev':
            SendWeatherMail().Dev_mode()
            logger.debug(f'{language["debug_done"]}')
            sys.exit(0)
        elif arg_test == 'free':
            SendWeatherMail().Free_mode()
            logger.debug(f'{language["debug_done"]}')
            sys.exit(0)
        elif arg_test == 'warning':
            SendWeatherMail().warning_send_mail()
            logger.debug(f'{language["debug_done"]}')
            sys.exit(0)

    _times = config['client-settings']['send-times']
    _mode = config['request-settings']['mode']

    #  另开一个进程与主进程同时运行 --> 运行loopCheck --> 循环检查本地时间是否与配置内时间相符
    multiprocessing.Process(target=loopCheck, args=(_mode, _times,)).run()

    # 循环检测时间 -> 每10分钟检查一次, 如果有则发送如果无则直接跳过
    loop_timer = 0
    while True:
        time.sleep(1)
        loop_timer += 1
        if loop_timer == 600:
            SendWeatherMail().warning_send_mail()
            loop_timer = 0
