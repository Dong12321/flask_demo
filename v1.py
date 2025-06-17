#!/user/bin/env python3
# -*- coding: utf-8 -*-
from flask import Flask, request, jsonify

# 创建flask对象
app = Flask(__name__)


# /xxx -> 执行index
@app.route("/index", methods=["POST", "GET"])
def index():
    age = request.args.get("age")
    pwd = request.args.get("pwd")
    print(age, pwd)

    xx = request.form.get("xx")
    yy = request.form.get("yy")
    print(xx, yy)

    print(request.json, type(request.json))
    return jsonify({"status": True, 'data': "test"})


# /yyy -> 执行home
@app.route("/home")
def home():
    return "home"


if __name__ == '__main__':
    app.run(host="127.0.0.1", port=5002)
