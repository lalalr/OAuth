# -*- coding: utf-8 -*-
import os
from flask_mysqldb import MySQL
from flask import Flask, redirect, url_for, render_template, request, abort, \
session, abort,  _app_ctx_stack, g
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
mysql = MySQL(app)

app.config.update(dict(
    SECRET_KEY = 'key',
    MYSQL_HOST = '3306'
    MYSQL_USER = 'root',
    MYSQL_PASSWORD = '123456',
    MYSQL_DB = 'user'
))

def get_db():
    top=_app_ctx_stack
    if not hasattr(g, 'mysql_db'):
        top.mysql_db = mysql.connect()
        top.mysql_db.row_factory = mysql.row
    return top.mysql_db
        

def init_db():
    pass

@app.teardown_appcontext
def close_db():
    top = _app_ctx_stack
    if hasattr(g,'mysql_db'):
        top.mysql_db.close()

def query_db(query, args=(), one=False):
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    return (rv[0] if rv else None) if one else rv

def get_user_id(username):
    rv = query_db('select user_id from user where username = ?',[username], one=True)
    return rv[0] if rv else None

@app.route('/')
def index():
    if  not session.get('logged_in'):
        message = "world"
    else:
        message = "admin"
    return render_template("index.html", message=message)

""" 
need check
"""
@app.route('/login', methods=["POST", "GET"])
def login():
    error=None
    if request.method == "POST":
        user = query_db('''select * from user where username = ?''', [request.form['username']], one = True)
        if user is None:
            error = "账号错误"
        elif not check_password_hash(user['pw_hash'],request.form['password']):
            error = "密码错误"
        else:
            session['logged_in'] = True
            return redirect(url_for("index"))
    return render_template("login.html", error=error)

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect(url_for("index"))

@app.route('/register', methods=['GET', 'POST'])
def register():
    error=None
    if request.method == 'POST':
        if not request.form['username']:
            error = "账号名为空"
        elif not request.form['password']:
            error = "密码为空"
        elif request.form['password'] != request.form['password2']:
            error = "与上面的密码不符"
        elif get_user_id(request.form['username']) is not None:
            error = "账号名已存在"
        else:
            db = get_db()
            db.execute('''insert into user (username, pw_hash) values (?, ?)''',
              [request.form['username'],
                generate_password_hash(request.form['password'])
                ])
            db.commit()
            return redirect(url_for('index'))
    return render_template('register.html', error=error)


if __name__ == '__main__':
    app.run(debug=True)