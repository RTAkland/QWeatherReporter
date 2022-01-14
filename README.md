<p align="center">
    <a href="https://github.com/MarkusJoe/QWeather">
        <img src="https://img.shields.io/badge/Python-3.10.x-blue.svg" alt="PythonVersion">
        <img src="https://img.shields.io/badge/release-3.2.3-green.svg" alt="QWeatherVersion">
        <img src="https://img.shields.io/badge/LINCESE-Apache2.0-orange.svg" alt="LICENSE">
    </a>
</p>

<div align="center">

## *QWeatherReporter*

<i style="text-align: center;"><a href="https://www.qweather.com/">QWeather Official Website</a></i>\
<i style="text-align: center;"><a href="https://dev.qweather.com/">QWeather Development Platform</a></i>

</div>

<div align="center">
<b><i>新增分支:GUI > 添加了界面</i></b><br>
<b><i>当前分支版本为重构后的版本重构前版本请在before分支中查看<br>(重构前版本不再更新,最新版本为v2.9.0)</i></b><br>
<b><i><a href="https://markusjoe.github.io/" target="_blank">点击跳转到帮助文档</a></i></b>
</div>

## 声明
- > 程序作者: **RTAkland (markushammered@gmail.com)**
- > 和风天气开发者平台：https://dev.qweather.com
- > 和风天气官网: https://qweather.com


### 开源
- 本项目以[Apache-2.0](./LICENSE)许可开源, 即:
  - 你可以直接使用该项目提供的功能, 无需任何授权
  - 你可以在**注明来源版权信息**的情况下对源代码进行任意分发和修改以及衍生

### 已实现功能
- [x] 发送免费版&开发版天气预报功能
- [x] 间隔10分钟请求一次自然灾害预警信息
- [x] 在网页上快速查看天气
- [x] 在邮件html内附带一句一言 
- [ ] ~~推送到QQ(咕咕咕)~~

### 问题汇总
#### Python 版本:
> 程序使用了*Python3.10.x*中的match-case语句
> 请使用*Python3.10.x*版本运行
#### 主题选择:
> 在2.9.0之后的版本不支持自定义天气图标 只能使用最新的图标
#### 配置填写问题:
> `location`项和`only-view-settings`类不需要用户填写, 只需要打开`QWeather.py`进行自助填写

## 如何使用
- 程序基于python3.10开发 务必使用python3.10版本运行
- 将config.yml正确填写完成
- 使用`pip/pip3 install -r requirements.txt` 安装需要的库
- 运行`QWeather.py`

### 网页上查看天气
- 将所有准备工作完成(能正常运行QWeather.py)
- 运行`QWeather.py`
- 打开浏览器输入**127.0.0.1:7898**
>127.0.0.1可以更改为部署本项目的服务器ip, 7898端口不能被其他程序占用或不开放此端口


## 联系方式
 - 邮箱: <markushammered@gmail.com>

