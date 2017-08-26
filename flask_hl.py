# -*- coding: utf-8 -*-
import os
from flask import Flask, redirect, url_for, render_template, request, abort

app = Flask(__name__)

app.config.update(dict(
    USERNAME = 'admin',
    PASSWORD = '123'
))

@app.route('/')
def index():
    return "Hello,World"

@app.route('/login', methods=["POST", "GET"])
def login():
    if request.method == "POST":
        if request.form["username"] != app.config["USERNAME"] and request.form["password"] != app.config["PASSWORD"]:
            abort(401)
    return render_template("login.html")


if __name__ == '__main__':
    app.run()