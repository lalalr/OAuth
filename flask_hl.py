# -*- coding: utf-8 -*-
from flask import Flask, redirect, url_for, render_template, request, abort, \
session
from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, VARCHAR
from sqlalchemy.ext.declarative import declarative_base
import bcrypt

app = Flask(__name__)
engine = create_engine('mysql+pymysql://root:W!1234@localhost/test')
Base = declarative_base()

app.config.update(dict(
    SECRET_KEY = 'key',
))

class User(Base):
    __tablename__ = 'users'
    user_id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(VARCHAR(16), unique=True)
    password = Column(VARCHAR(32))

    def __init__(self, username, plaintext_password):
        self.username = username
        self.password = plaintext_password
"""
    def verify_password(self, password):
        pwhash = bcrypt.hashpw(password, self.password)
        return self.password == pwhash
"""

@app.route('/')
def index():
    if  not session.get('logged_in'):
        message = "world"
    else:
        message = "admin"
    return render_template("index.html", message=message)

@app.route('/login', methods=["POST", "GET"])
def login():
    error=None
    if request.method == "POST":
        user = User.query.filter_by(request.form['username']).first()
        if user is None:
            error = "账号错误"
        elif not User.verify_password(request.form['passworld']):
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
##
        elif User.query.filter_by(request.form['username']).first() is not None:

            error = "账号名已存在"
        else:
            new_user = User(request.form['username'], request.form['password'])
            session.add(new_user)
            session.commit()
            return redirect(url_for('index'))
    return render_template('register.html', error=error)


if __name__ == '__main__':
    app.run(debug=True)