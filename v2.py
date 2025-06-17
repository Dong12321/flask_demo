#!/user/bin/env python3
# -*- coding: utf-8 -*-
import hashlib
from flask import Flask, request, jsonify

# 创建flask对象
app = Flask(__name__)


# /xxx -> 执行index
@app.route("/bili", methods=["POST"])
def bili():
    """
    请求的数据格式要求：{”ordered_string“:"....."}
    :return:
    """
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
