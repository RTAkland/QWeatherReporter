#!/usr/bin/env python3
# -- coding:utf-8 --
# @Author: markushammered@gmail.com
# @Development Tool: PyCharm
# @Create Time: 2021/12/15
# @File Name: information.py

import requests
from core.read_config import read_config


class WeatherInfo:
    def __init__(self):
        self.config = read_config()
        self.dev = 'https://devapi.qweather.com/v7/weather/7d'
        self.free = 'https://devapi.qweather.com/v7/weather/3d'
        self.warning = 'https://devapi.qweather.com/v7/warning/now'
        self.key = self.config[1]['key']
        self.location = self.config[1]['location']
        self.unit = self.config[1]['unit']
        self.language = self.config[1]['lang']
        self.params = {'location': self.location,
                       'key': self.key,
                       'unit': self.unit,
                       'lang': self.language}
        self.session = requests.Session()
        self.session.trust_env = False

    def dev_version(self):
        """
        Developer's Qweather version
        :return: dates, day_weathers, night_weathers, highest_temps, lowest_temps,
        icon_list, sunset, sunrise, humidity, wind_speed, wind_scale, wind_dir, ultraviolet_rays, cloud, pressure, vis
        """
        dev_res = self.session.get(self.dev, params=self.params).json()

        day_1 = dev_res['daily'][0]
        day_2 = dev_res['daily'][1]
        day_3 = dev_res['daily'][2]
        day_4 = dev_res['daily'][3]
        day_5 = dev_res['daily'][4]
        day_6 = dev_res['daily'][5]
        day_7 = dev_res['daily'][6]

        dates = [day_1['fxDate'][5:], day_2['fxDate'][5:], day_3['fxDate'][5:], day_4['fxDate'][5:],
                 day_5['fxDate'][5:],
                 day_6['fxDate'][5:],
                 day_7['fxDate'][5:]]
        day_weathers = [day_1['textDay'], day_2['textDay'], day_3['textDay'], day_4['textDay'], day_5['textDay'],
                        day_6['textDay'], day_7['textDay']]
        night_weathers = [day_1['textNight'], day_2['textNight'], day_3['textNight'], day_4['textNight'],
                          day_5['textNight'], day_6['textNight'], day_7['textNight']]
        highest_temps = [day_1['tempMax'], day_2['tempMax'], day_3['tempMax'], day_4['tempMax'], day_5['tempMax'],
                         day_6['tempMax'], day_7['tempMax']]
        lowest_temps = [day_1['tempMin'], day_2['tempMin'], day_3['tempMin'], day_4['tempMin'], day_5['tempMin'],
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

        return dates, day_weathers, night_weathers, highest_temps, lowest_temps, icon_list, sunset, sunrise, humidity, \
               wind_speed, wind_scale, wind_dir, ultraviolet_rays, cloud, pressure, vis

    def free_version(self):
        """
        
        :return: return dates, day_weathers, night_weathers, highest_temps, lowest_temps, icon_list, sunset, sunrise, 
        humidity, wind_speed, wind_scale, wind_dir, ultraviolet_rays, cloud, pressure, vis 
        """

        free_res = self.session.get(self.free, params=self.params).json()
        
        day_1 = free_res['daily'][0]
        day_2 = free_res['daily'][1]
        day_3 = free_res['daily'][2]

        dates = [day_1['fxDate'][5:], day_2['fxDate'][5:], day_2['fxDate'][5:]]
        day_weathers = [day_1['textDay'], day_2['textDay'], day_2['textDay']]
        night_weathers = [day_1['textNight'], day_2['textNight'], day_2['textNight']]
        highest_temps = [day_1['tempMax'], day_2['tempMax'], day_3['tempMax']]
        lowest_temps = [day_1['tempMin'], day_2['tempMin'], day_2['tempMin']]
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

        return dates, day_weathers, night_weathers, highest_temps, lowest_temps, icon_list, sunset, sunrise, humidity, \
               wind_speed, wind_scale, wind_dir, ultraviolet_rays, cloud, pressure, vis
    
    def warning_(self):
        """

        :return: release_time, title, status, level, type_, text, start_time, end_time
        """
        warning_res = self.session.get(self.warning, params=self.params).json()

        release_time = warning_res['warning'][0]['pubTime'][:10]
        title = warning_res['warning'][0]['title']
        status = warning_res['warning'][0]['status']
        level = warning_res['warning'][0]['level']
        type_ = warning_res['warning'][0]['typeName']
        text = warning_res['warning'][0]['text']
        start_time = warning_res['warning'][0]['startTime']
        end_time = warning_res['warning'][0]['endTime']
        match start_time, end_time:
            case None, None:
                start_time, end_time = None, None
            case _:
                pass

        return release_time, title, status, level, type_, text, start_time, end_time

