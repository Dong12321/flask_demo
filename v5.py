#!/user/bin/env python3
# -*- coding: utf-8 -*-
import hashlib
import pymysql
from flask import Flask, request, jsonify
from dbutils.pooled_db import PooledDB

# 创建flask对象
app = Flask(__name__)

Pool = PooledDB(
    creator=pymysql,  # 使用链接数据库的模块
    maxconnections=10,  # 连接池允许的最大连接数,0和None表示不限制连接数
    mincached=2,  # 初始化时，链接池中至少创建的空闲的链接，0表示不创建
    maxcached=5,  # 链接池中最多闲置的链接，0和None不限制
    blocking=True,  # 连接池中如果没有可用连接后，是否阻塞等待。True，等待;False，不等待然后报错
    setsession=[],  # 开始会话前执行的命令列表。如:["set datestyle to"set time zone...."]
    ping=0,
    host='127.0.0.1', port=3306, user='root', passwd='1234', charset='utf8mb4', db='flask_demo'
)


def fetch_one(sql, params):
    # conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='1234', charset='utf8mb4', db='flask_demo')
    conn = Pool.connection()
    cursor = conn.cursor()
    result = cursor.execute(sql, params)
    cursor.close()
    conn.close()  # 将此链接交还给连接池
    return result


# /xxx -> 执行index
@app.route("/bili", methods=["POST"])
def bili():
    """
    请求的URL需要带TOKEN，/bili?token=7a11bc06-3c5a-4eb4-8869-dc2bc905a6df
    请求的数据格式要求：{”ordered_string“:"....."}
    :return:
    """
    # 1.token 是否为空
    token = request.args.get("token")
    if not token:
        return jsonify({"status": False, 'error': "认证失败"})

    # 2. token是否合法

    result = fetch_one("select * from user where token = %s", [token, ])
    if not result:
        return jsonify({"status": False, 'error': "认证失败"})

    ordered_string = request.json.get("ordered_string")
    if not ordered_string:
        return jsonify({"status": False, 'error': "参数错误"})

    # 调用核心算法，生成sign签名
    encrypt_string = ordered_string + "560c52ccd288fed045859ed18bffd973"
    obj = hashlib.md5(encrypt_string.encode('utf-8'))
    sign = obj.hexdigest()
    return jsonify({"status": True, 'data': sign})


if __name__ == '__main__':
    app.run(host="127.0.0.1", port=5002)
