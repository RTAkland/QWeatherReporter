#!/usr/bin/env python3
# -- coding:utf-8 --
# @Author: markushammered@gmail.com
# @Development Tool: PyCharm
# @Create Time: 2021/12/18
# @File Name: webservice.py


import socket
import threading
from core.logger import Logger
from core.read_config import read_config
from core.information import WeatherInfo
from core.language import Language

try:
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind(('0.0.0.0', 7898))
    server.listen(5)
except OSError as e:
    Logger.critical(e)

language = Language()


def build_html():
    """
    构建html主体
    :return:
    """
    settings = read_config()
    city = settings[3]['city-name']
    mode = settings[1]['mode']
    match mode:
        case 'dev':
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

            html = f"""
                <!DOCTYPE html>
                <html lang="en">
                <head>
                    <meta charset="UTF-8">
                    <title>QWeather|网页查看天气服务</title>
                </head>
                <body>
                <p style="text-align: center"><i><b>地区:{city}</b></i></p>
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
                        <td>{day_weathers[0]}<img src="./res/icons/{icons[0]}.png" width="20" alt="">/{night_weathers[0]}
                        <img src="./res/icons/{icons[1]}.png" 
                        width="20" alt=""></td> <td>{lowest_temps[0]}℃</td> 
                        <td>{highest_temps[0]}℃</td>
                    </tr>
                    <tr>
                        <td>{dates[1]}</td>
                        <td>{day_weathers[1]}<img src="./res/icons/{icons[2]}.png" width="20" alt="">/{night_weathers[1]}
                        <img src="./res/icons/{icons[3]}.png" 
                        width="20" alt=""></td> <td>{lowest_temps[1]}℃</td> 
                        <td>{highest_temps[1]}℃</td>
                    </tr>
                        <tr>
                        <td>{dates[2]}</td>
                        <td>{day_weathers[2]}<img src="./res/icons/{icons[4]}.png" width="20" alt="">/{night_weathers[2]}
                        <img src="./res/icons/{icons[5]}.png" 
                        width="20" alt=""></td> <td>{lowest_temps[2]}℃</td> 
                        <td>{highest_temps[2]}℃</td>
                    </tr>
                        <tr>
                        <td>{dates[3]}</td>
                        <td>{day_weathers[3]}<img src="./res/icons/{icons[6]}.png" width="20" alt="">/{night_weathers[3]}
                        <img src="./res/icons/{icons[7]}.png" 
                        width="20" alt=""></td> <td>{lowest_temps[3]}℃</td> 
                        <td>{highest_temps[3]}℃</td>
                    </tr>
                        <tr>
                        <td>{dates[4]}</td>
                        <td>{day_weathers[4]}<img src="./res/icons/{icons[8]}.png" width="20" alt="">/{night_weathers[4]}
                        <img src="./res/icons/{icons[9]}.png" 
                        width="20" alt=""></td> <td>{lowest_temps[4]}℃</td> 
                        <td>{highest_temps[4]}℃</td>
                    </tr>
                        <tr>
                        <td>{dates[5]}</td>
                        <td>{day_weathers[5]}<img src="./res/icons/{icons[10]}.png" width="20" alt="">/{night_weathers[5]}
                        <img src="./res/icons/{icons[11]}.png" 
                        width="20" alt=""></td> <td>{lowest_temps[5]}℃</td> 
                        <td>{highest_temps[5]}℃</td>
                    </tr>
                        <tr>
                        <td>{dates[6]}</td>
                        <td>{day_weathers[6]}<img src="./res/icons/{icons[12]}.png" width="20" alt="">/{night_weathers[6]}
                        <img src="./res/icons/{icons[13]}.png" 
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
                        <td><img src="./res/basic-resources/sunrise.png" alt="Sunrise" width="30"></td>
                        <td>&nbsp;</td>
                        <td><img src="./res/basic-resources/sunset.png" alt="Sunset" width="30"></td>
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
                </div>
                </body>
                </html>"""
            return html
        case 'free':
            dev_weather = WeatherInfo().free_version()
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

            html = f"""
                    <!DOCTYPE html>
                    <html lang="en">
                    <head>
                        <meta charset="UTF-8">
                        <title>QWeather|网页查看天气服务</title>
                    </head>
                    <body>
                    <p style="text-align: center"><i><b>地区:{city}</b></i></p>
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
                            <td>{day_weathers[0]}<img src="./res/icons/{icons[0]}.png" width="20" alt="">/{night_weathers[0]}
                            <img src="./res/icons/{icons[1]}.png" 
                            width="20" alt=""></td> <td>{lowest_temps[0]}℃</td> 
                            <td>{highest_temps[0]}℃</td>
                        </tr>
                        <tr>
                            <td>{dates[1]}</td>
                            <td>{day_weathers[1]}<img src="./res/icons/{icons[2]}.png" width="20" alt="">/{night_weathers[1]}
                            <img src="./res/icons/{icons[3]}.png" 
                            width="20" alt=""></td> <td>{lowest_temps[1]}℃</td> 
                            <td>{highest_temps[1]}℃</td>
                        </tr>
                            <tr>
                            <td>{dates[2]}</td>
                            <td>{day_weathers[2]}<img src="./res/icons/{icons[4]}.png" width="20" alt="">/{night_weathers[2]}
                            <img src="./res/icons/{icons[5]}.png" 
                            width="20" alt=""></td> <td>{lowest_temps[2]}℃</td> 
                            <td>{highest_temps[2]}℃</td>
                    </table>
                    <table style="border: 0;text-align: center; margin:0 auto">
                        <tr>
                            <th>&nbsp;</th>
                        </tr>
                        <tr>
                            <th>风速/风级/风向</th>
                            <th>相对湿度</th>
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
                            <td><img src="./res/basic-resources/sunrise.png" alt="Sunrise" width="30"></td>
                            <td>&nbsp;</td>
                            <td><img src="./res/basic-resources/sunset.png" alt="Sunset" width="30"></td>
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
                    </div>
                    </body>
                    </html>"""
            return html
        case _:
            return "You hadn't selected a mode"


def process_requests(c, a):
    """
    处理请求
    :param c: connection
    :param a: address
    :return:
    """
    try:
        data = str(c.recv(1024)).split(':')[0][6:][:-17]
        html = build_html()
        if data == '/':  # 判断用户请求的目标是否为根目录, 如果是则返回html; 如果不是则继续判断
            c.send('HTTP/1.1 200 OK\r\n\r\n'.encode('utf-8'))
            c.send(html.encode('utf-8'))
            Logger.info(f'{language["get_resource"]} {data} {language["get_resource_from"]} {a[0]}:{a[1]}')
        try:
            with open(f'./{data}', 'rb') as f:
                c.send('HTTP/1.1 200 OK\r\n\r\n'.encode('utf-8'))
                c.send(f.read())
                Logger.info(f'{language["get_resource"]} {data} {language["get_resource_from"]} {a[0]}:{a[1]}')
        except FileNotFoundError:
            with open('./res/basic-resources/404.html', 'r') as not_found:
                c.send(f'HTTP/1.1 404 Not Found\r\n\r\n{not_found.read()}'.encode('utf-8'))
    except BrokenPipeError:
        Logger.error(f'{language["connection_speed_too_fast"]}')
    finally:
        c.close()
        return


def accept_requests():
    """
    接受请求
    :return:
    """
    while True:
        c, a = server.accept()
        threading.Thread(target=process_requests, args=(c, a,)).start()
