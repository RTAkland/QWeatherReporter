#!/usr/bin/env python3
# -- coding:utf-8 --
# @Author: markushammered@gmail.com
# @Development Tool: PyCharm
# @Create Time: 2022/1/9
# @File Name: buildGUIClass.py
import tkinter
import tkinter as tk

root = tk.Tk()
root.title('QWeather client')
sw = root.winfo_screenwidth()
sh = root.winfo_screenheight()
ww = 700
wh = 490
x = (sw - ww) / 2
y = (sh - wh) / 2
root.geometry("%dx%d+%d+%d" % (ww, wh, x, y))
root.minsize(700, 490)
root.maxsize(700, 490)

log_label = tk.Label(root, text='Log information')
log_label.place(x=170, y=4)
log_text = tk.Text(root, width=55, height=15)
log_text.place(x=30, y=30)
var_command = tk.StringVar()


class InsertLog:
    def __init__(self):
        self.log_text = log_text

    def insert(self, msg: str):
        """
        insert the information to gui(Text)
        :param msg: information
        :return:
        """
        if '\n' not in msg:
            msg = msg + '\n'
        self.log_text.configure(state=tkinter.NORMAL)  # writable
        self.log_text.insert('insert', msg)  # insert information
        self.log_text.configure(state=tkinter.DISABLED)  # readable


class Features:
    def __init__(self):
        self.root = root
        self.tk = tk
        self.log_text = log_text

    def quit_(self):
        """
        quit gui
        :return:
        """
        self.root.destroy()
        self.root.quit()
