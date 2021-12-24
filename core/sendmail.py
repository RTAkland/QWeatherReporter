#!/usr/bin/env python3
# -- coding:utf-8 --
# @Author: markushammered@gmail.com
# @Development Tool: PyCharm
# @Create Time: 2021/12/16
# @File Name: sendmail.py


import sys
import smtplib
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.header import Header
from email.mime.text import MIMEText
from core.logger import Logger
from core.language import Language
from core.information import WeatherInfo
from core.read_config import read_config
from lib.hitokoto import hitokoto


class Mail:
    def __init__(self):
        self.settings = read_config()
        self.language = Language()
        self.enableSSL = self.settings[2]['SSL']
        self.server = self.settings[0]['server']
        self.port = self.settings[0]['port']
        self.password = self.settings[0]['password']
        self.sender = self.settings[0]['sender']
        self.receiver = self.settings[1]['receiver']
        self.city_name = self.settings[3]['city-name']
        self.message = MIMEMultipart('related')
        self.message['From'] = Header('QWeather')  # 发件人名称
        self.message['To'] = Header('All allowed User')  # 收件人显示名称

        self.hitokoto = hitokoto()  # 一言

        if self.enableSSL:
            self.smtp = smtplib.SMTP_SSL(self.server, self.port)  # 登录服务器 使用SSL连接
        else:
            self.smtp = smtplib.SMTP(self.server, self.port)  # 登录邮箱服务器 不使用SSL连接

    def dev_version(self):
        """
        开发者版本
        :return:
        """
        dev_weather = WeatherInfo().dev_version()
        dates = dev_weather[0]
        day_weathers = dev_weather[1]
        night_weathers = dev_weather[2]
        highest_temps = dev_weather[3]
        lowest_temps = dev_weather[4]
        icons = dev_weather[5]
        sunset = dev_weather[6]
        sunrise = dev_weather[7]
        humidity = dev_weather[8]
        wind_speed = dev_weather[9]
        wind_scale = dev_weather[10]
        wind_dir = dev_weather[11]
        uv_index = dev_weather[12]
        cloud = dev_weather[13]
        pressure = dev_weather[14]
        vis = dev_weather[15]

        mail_html = f"""
                <p style="text-align: center">
                    <i>
                        <b>
                            地区:{self.city_name}
                            <br>
                            发送者:{self.sender}
                        </b>
                    </i>
                </p>
                <br />
                <table style="border: 0; text-align: center; margin:0 auto">
                    <tr>
                        <th>|&nbsp;日期&nbsp;&nbsp;</th>
                        <th>|&nbsp;天气&nbsp;&nbsp;</th>
                        <th>|&nbsp;最低温度&nbsp;&nbsp;</th>
                        <th>|&nbsp;最高温度&nbsp;&nbsp;</th>
                    </tr>
                    <tr>
                        <!--日期 天气 最低 最高/Date Weather LowestTemp HighestTemp-->
                        <td>今天</td>
                        <td>{day_weathers[0]}<img src="cid:img1" width="20" alt="">/{night_weathers[0]}<img src="cid:img2" 
                        width="20" alt=""></td> <td>{lowest_temps[0]}℃</td> 
                        <td>{highest_temps[0]}℃</td>
                    </tr>
                    <tr>
                        <td>{dates[1]}</td>
                        <td>{day_weathers[1]}<img src="cid:img3" width="20" alt="">/{night_weathers[1]}<img src="cid:img4" 
                        width="20" alt=""></td> <td>{lowest_temps[1]}℃</td> 
                        <td>{highest_temps[1]}℃</td>
                    </tr>
                        <tr>
                        <td>{dates[2]}</td>
                        <td>{day_weathers[2]}<img src="cid:img5" width="20" alt="">/{night_weathers[2]}<img src="cid:img6" 
                        width="20" alt=""></td> <td>{lowest_temps[2]}℃</td> 
                        <td>{highest_temps[2]}℃</td>
                    </tr>
                        <tr>
                        <td>{dates[3]}</td>
                        <td>{day_weathers[3]}<img src="cid:img7" width="20" alt="">/{night_weathers[3]}<img src="cid:img8" 
                        width="20" alt=""></td> <td>{lowest_temps[3]}℃</td> 
                        <td>{highest_temps[3]}℃</td>
                    </tr>
                        <tr>
                        <td>{dates[4]}</td>
                        <td>{day_weathers[4]}<img src="cid:img9" width="20" alt="">/{night_weathers[4]}<img src="cid:img10" 
                        width="20" alt=""></td> <td>{lowest_temps[4]}℃</td> 
                        <td>{highest_temps[4]}℃</td>
                    </tr>
                        <tr>
                        <td>{dates[5]}</td>
                        <td>{day_weathers[5]}<img src="cid:img11" width="20" alt="">/{night_weathers[5]}<img src="cid:img12" 
                        width="20" alt=""></td> <td>{lowest_temps[5]}℃</td> 
                        <td>{highest_temps[5]}℃</td>
                    </tr>
                        <tr>
                        <td>{dates[6]}</td>
                        <td>{day_weathers[6]}<img src="cid:img13" width="20" alt="">/{night_weathers[6]}<img src="cid:img14" 
                        width="20" alt=""></td> <td>{lowest_temps[6]}℃</td> 
                        <td>{highest_temps[6]}℃</td>
                    </tr>
                </table>
                <table style="border: 0;text-align: center; margin:0 auto">
                    <tr>
                        <th>&nbsp;</th>
                    </tr>
                    <tr>
                        <th>风速/级/向</th>
                        <th>湿度</th>
                        <th>紫外线</th>
                    </tr>
                    <tr>
                        <td>{wind_speed}m/s&nbsp; {wind_scale}&nbsp; {wind_dir}&nbsp;</td>
                        <td>{humidity}%&nbsp;</td>
                        <td>{uv_index}&nbsp;</td>
                    </tr>
                    <tr>
                        <th>&nbsp;</th>
                    </tr>
                    <tr>
                        <th>能见度</th>
                        <th>压强</th>
                        <th>云量</th>
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
                <br />
                <div style="text-align: center" id="hitokoto">
                    <p>
                        {self.hitokoto}
                    </p>
                </div>
                <div style="text-align: center;" id="About">
                    <br />
                    <i>
                        <b>
                            <a href="https://dev.qweather.com/" style="color: black" target="_blank">QWeather</a>
                            <a style="color: black">&nbsp;·&nbsp;</a>
                            <a href="https://github.com/MarkusJoe/QWeather" style="color: black" target="_blank">Github Repo</a>
                        </b>
                    </i>
                </div>"""
        self.message['Subject'] = '七天天气预报'  # 邮件标题
        self.message.attach(MIMEText(mail_html, 'html', 'utf-8'))

        image_count = 1
        for image_resource in icons:
            with open(f'./res/icons/{image_resource}.png', 'rb') as fp:
                MyImage = MIMEImage(fp.read())
                MyImage.add_header('Content-ID', f'img{image_count}')
                self.message.attach(MyImage)
                image_count += 1

        with open('./res/basic-resources/sunrise.png', 'rb') as sr_f:
            sunrise_img = MIMEImage(sr_f.read())
            sunrise_img.add_header('Content-ID', 'sunrise')
            self.message.attach(sunrise_img)
        with open('./res/basic-resources/sunset.png', 'rb') as ss_f:
            sunset_img = MIMEImage(ss_f.read())
            sunset_img.add_header('Content-ID', 'sunset')
            self.message.attach(sunset_img)

        try:
            self.smtp.login(self.sender, self.password)  # 登录
            self.smtp.sendmail(self.sender, self.receiver, self.message.as_string())  # 发送
            Logger.info(f'{self.language["mail_succeed"]}')
        except smtplib.SMTPException as e:  # 处理错误
            Logger.critical(f'{self.language["mail_error"]}: {e}')
            sys.exit(1)

    def free_version(self):
        """
        免费版本
        :return:
        """
        free_weather = WeatherInfo().free_version()
        dates = free_weather[0]
        day_weathers = free_weather[1]
        night_weathers = free_weather[2]
        highest_temps = free_weather[3]
        lowest_temps = free_weather[4]
        icons = free_weather[5]
        sunset = free_weather[6]
        sunrise = free_weather[7]
        humidity = free_weather[8]
        wind_speed = free_weather[9]
        wind_scale = free_weather[10]
        wind_dir = free_weather[11]
        uv_index = free_weather[12]
        cloud = free_weather[13]
        pressure = free_weather[14]
        vis = free_weather[15]

        mail_html = f"""
                <p style="text-align: center">
                    <i>
                        <b>
                            地区:{self.city_name}
                            <br>
                            发送者:{self.sender}
                        </b>
                    </i>
                </p>
                <br />
                <table style="border: 0; text-align: center; margin:0 auto">
                    <tr>
                        <th>|&nbsp;日期&nbsp;&nbsp;</th>
                        <th>|&nbsp;天气&nbsp;&nbsp;</th>
                        <th>|&nbsp;最低温度&nbsp;&nbsp;</th>
                        <th>|&nbsp;最高温度&nbsp;&nbsp;</th>
                    </tr>
                    <tr>
                        <!--日期 天气 最低 最高/Date Weather LowestTemp HighestTemp-->
                        <td>今天</td>
                        <td>{day_weathers[0]}<img src="cid:img1" width="20" alt="">/{night_weathers[0]}<img src="cid:img2" 
                        width="20" alt=""></td> <td>{lowest_temps[0]}℃</td> 
                        <td>{highest_temps[0]}℃</td>
                    </tr>
                    <tr>
                        <td>{dates[1]}</td>
                        <td>{day_weathers[1]}<img src="cid:img3" width="20" alt="">/{night_weathers[1]}<img src="cid:img4" 
                        width="20" alt=""></td> <td>{lowest_temps[1]}℃</td> 
                        <td>{highest_temps[1]}℃</td>
                    </tr>
                        <tr>
                        <td>{dates[2]}</td>
                        <td>{day_weathers[2]}<img src="cid:img5" width="20" alt="">/{night_weathers[2]}<img src="cid:img6" 
                        width="20" alt=""></td> <td>{lowest_temps[2]}℃</td> 
                        <td>{highest_temps[2]}℃</td>
                </table>
                <table style="border: 0;text-align: center; margin:0 auto">
                    <tr>
                        <th>&nbsp;</th>
                    </tr>
                    <tr>
                        <th>风速/级/向</th>
                        <th>湿度</th>
                        <th>紫外线</th>
                    </tr>
                    <tr>
                        <td>{wind_speed}m/s&nbsp; {wind_scale}&nbsp; {wind_dir}&nbsp;</td>
                        <td>{humidity}%&nbsp;</td>
                        <td>{uv_index}&nbsp;</td>
                    </tr>
                    <tr>
                        <th>&nbsp;</th>
                    </tr>
                    <tr>
                        <th>能见度</th>
                        <th>压强</th>
                        <th>云量</th>
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
                <br />
                <div style="text-align: center" id="hitokoto">
                    <p>
                        {self.hitokoto}
                    </p>
                </div>
                <div style="text-align: center;" id="About">
                    <br />
                    <i>
                        <b>
                            <a href="https://dev.qweather.com/" style="color: black" target="_blank">QWeather</a>
                            <a style="color: black">&nbsp;·&nbsp;</a>
                            <a href="https://github.com/MarkusJoe/QWeather" style="color: black" target="_blank">Github Repo</a>
                        </b>
                    </i>
                </div>"""
        self.message['Subject'] = '三天天气预报'  # 邮件标题
        self.message.attach(MIMEText(mail_html, 'html', 'utf-8'))

        image_count = 1
        for image_resource in icons:
            with open(f'./res/icons/{image_resource}.png', 'rb') as fp:
                MyImage = MIMEImage(fp.read())
                MyImage.add_header('Content-ID', f'img{image_count}')
                self.message.attach(MyImage)
                image_count += 1

        with open('./res/basic-resources/sunrise.png', 'rb') as sr_f:
            sunrise_img = MIMEImage(sr_f.read())
            sunrise_img.add_header('Content-ID', 'sunrise')
            self.message.attach(sunrise_img)
        with open('./res/basic-resources/sunset.png', 'rb') as ss_f:
            sunset_img = MIMEImage(ss_f.read())
            sunset_img.add_header('Content-ID', 'sunset')
            self.message.attach(sunset_img)

        try:
            self.smtp.login(self.sender, self.password)  # 登录
            self.smtp.sendmail(self.sender, self.receiver, self.message.as_string())  # 发送
            Logger.info(f'{self.language["mail_succeed"]}')
        except smtplib.SMTPException as e:  # 处理错误
            Logger.critical(f'{self.language["mail_error"]}: {e}')
            sys.exit(1)

    def warning_(self):
        """
        自然灾害预警
        :return:
        """
        info = WeatherInfo().warning_()
        release_time = info[0]
        title = info[1]
        status = info[2]
        level = info[3]
        type_ = info[4]
        text = info[5]
        start_time = info[6]
        end_time = info[7]

        match status:
            case 'update':
                status = '预警更新'
                Logger.info(f'{self.language["new_warning"]}')
            case 'active':
                status = '已有灾害'
                Logger.info(f'{self.language["warning_updated"]}')
            case 'cancel':
                Logger.info(f'{self.language["warning_canceled"]}')

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
                        <h3>释放时间:{release_time} {level}级</h3>
                        <p>
                            预警状态:{status} 预警类型:{type_} 灾害持续时间:{start_time[:10]}~{end_time[:10]}
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
        self.message['Subject'] = '自然灾害预警'  # 邮件标题
        self.message.attach(MIMEText(mail_html, 'html', 'utf-8'))

        with open('./res/basic-resources/sunrise.png', 'rb') as sr_f:
            sunrise_img = MIMEImage(sr_f.read())
            sunrise_img.add_header('Content-ID', 'sunrise')
            self.message.attach(sunrise_img)
        with open('./res/basic-resources/sunset.png', 'rb') as ss_f:
            sunset_img = MIMEImage(ss_f.read())
            sunset_img.add_header('Content-ID', 'sunset')
            self.message.attach(sunset_img)

        try:
            if status != 'cancel':
                self.smtp.login(self.sender, self.password)  # 登录
                self.smtp.sendmail(self.sender, self.receiver, self.message.as_string())  # 发送
                Logger.info(f'{self.language["mail_succeed"]}')
        except smtplib.SMTPException as e:  # 处理错误
            Logger.critical(f'{self.language["mail_error"]}: {e}')
            sys.exit(1)
