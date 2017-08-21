# -*- coding: utf-8 -*-
import os
from flask import Flask, redirect, url_for

app = Flask(__name__)

app.config.update(dict(
    USERNAME = 'admin',
    PASSWORD = '123'
))

@app.route('/')
def index():
    return "Hello,World"
'''
@app.route('/login')
def login():
    error = None
    if username != app.config['USERNAME']:
        error = "用户名出错"
    elif password != app.config['PASSWORD']:
        error = "密码错误"
    else:
        return render_template('login.html',username=username,password=password)
'''

if __name__ == '__main__':
    app.run()