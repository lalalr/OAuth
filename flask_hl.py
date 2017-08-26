# -*- coding: utf-8 -*-
import os
from flask import Flask, redirect, url_for, render_template, request, abort, session, abort

app = Flask(__name__)

app.config.update(dict(
    USERNAME = 'admin',
    PASSWORD = '123',
    SECRET_KEY = 'key'
))

@app.route('/')
def index():
    if  not session.get('logged_in'):
        message = "world"
    else:
        message = "admin"
    return render_template("index.html", message=message)

@app.route('/login', methods=["POST", "GET"])
def login():
    if request.method == "POST":
        if request.form["username"] != app.config["USERNAME"] or request.form["password"] != app.config["PASSWORD"]:
            abort(401)
        else:
            session['logged_in'] = True
            return redirect(url_for("index"))
    return render_template("login.html")

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect(url_for("index"))


if __name__ == '__main__':
    app.run(debug=True)