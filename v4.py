#!/user/bin/env python3
# -*- coding: utf-8 -*-
import hashlib
import pymysql
from flask import Flask, request, jsonify

# 创建flask对象
app = Flask(__name__)


def fetch_one(sql, params):
    conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='1234', charset='utf8mb4', db='flask_demo')
    cursor = conn.cursor()
    result = cursor.execute(sql, params)
    cursor.close()
    conn.close()
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
