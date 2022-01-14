#!/usr/bin/env python3
# -- coding:utf-8 --
# @Author: markushammered@gmail.com
# @Development Tool: PyCharm
# @Create Time: 2021/12/16
# @File Name: QWeather.py


import threading
from core import qweather
from tkinter import messagebox
from lib.buildGUIClass import tk
from lib.buildGUIClass import root
from lib.buildGUIClass import Features


def on_closing():
    if messagebox.askokcancel('Exit', 'Confirm exit?'):
        Features().quit_()


if __name__ == '__main__':
    b1 = tk.Button(root,
                   text='Click to run QWeather',
                   command=threading.Thread(target=qweather.main, name='main').start)
    b1.place(x=45, y=300)
    b2 = tk.Button(root,
                   text='Exit the main program',
                   command=on_closing)
    b2.place(x=275, y=300)
    l1 = tk.Label(root,
                  text='更多功能敬请期待\nEnjoy this ~',)
    l1.place(x=530, y=70)
    information = """
    已知问题:
    1.开启QWeather主程序后退出只会退出界面主程序并不会退出
    2.webservice.py 的输出并不会被插入到GUI界面里
    * 更多问题待发现...
    """
    l2 = tk.Label(root,
                  text=information)
    l2.place(x=140, y=350)
    root.protocol('WM_DELETE_WINDOW', on_closing)
    root.mainloop()
