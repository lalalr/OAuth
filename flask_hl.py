# -*- coding: utf-8 -*-
import sys
from flask import Flask, redirect, url_for, render_template, request, session
from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, VARCHAR
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from werkzeug.security import check_password_hash, generate_password_hash

app = Flask(__name__)
engine = create_engine('mysql+pymysql://root:123456@localhost/test')
Base = declarative_base()
Session = sessionmaker(bind=engine)
sess = Session()
reload(sys)
sys.setdefaultencoding('utf-8')

app.config.update(dict(
    SECRET_KEY = 'key',
))

class User(Base):
    __tablename__ = 'users'
    user_id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(VARCHAR(16), unique=True)
    password = Column(VARCHAR(128))
    sex = Column(Integer)
    nickname = Column(VARCHAR(16))

    def __init__(self, username, plaintext_password, sex, nickname):
        self.username = username
        self.set_pw(plaintext_password)
        self.setSex(sex)
        self.setNick(nickname)

    def __repr__(self):
        return "<users(user_id='%s', username='%s', password='%s', sex='%s', nickname='%s')>" % (
            self.user_id, self.username, self.password, self.sex, self.nickname)

    def set_pw(self, plaintext_password):
        self.password = generate_password_hash(plaintext_password)

    def check_pw(self, plaintext_password):
        return check_password_hash(self.password, plaintext_password)

    def setSex(self, sex):
        self.sex = sex

    def setNick(self, nickname):
        self.nickname = nickname

@app.route('/')
def index():

    nick = ''
    sex = 2
    message = ''
    if session.get('logged_in'):
        nick = session.get('nick')
        sex = session.get('sex')
        message='回来'
    else:
        nick = '新人'
        message=''
    return render_template("index.html", nick=nick,sex=sex,message=message)

@app.route('/login', methods=["POST", "GET"])
def login():
    error=None
    if request.method == "POST":
        query = sess.query(User).filter(User.username == request.form['username'])
        if query.count() == 0:
            error = "账号错误"
        else:
            user = query.first()
            if not user.check_pw(request.form['password']):
                error = "密码错误"
            else:
                session['logged_in'] = True
                session['nick'] = user.nickname
                session['sex'] = user.sex
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
        elif sess.query(User).filter(User.username == request.form['username']).count() != 0:
            error = "账号名已存在"
        else:
            new_user = User(request.form['username'], request.form['password'], request.form['sex'], request.form['nick'])
            sess.add(new_user)
            sess.commit()
            return redirect(url_for('index'))
    return render_template('register.html', error=error)

if __name__ == '__main__':
    app.run(debug=True)