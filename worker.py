#!/user/bin/env python3
# -*- coding: utf-8 -*-
import hashlib
import redis
import json

"""
去队列中获取任务，执行并写入到结果队列
"""

def get_task():
    REDIS_CONN_PARAMS = {
        "host": "127.0.0.1",
        "password": "1234",
        "port": "6379",
        "encoding": "utf-8"
    }
    conn = redis.Redis(**REDIS_CONN_PARAMS)
    data = conn.brpop("spider_task_list", timeout=10)
    if not data:
        return
    return data[1].decode('utf-8')

def set_result(tid, value):
    REDIS_CONN_PARAMS = {
        "host": "127.0.0.1",
        "password": "1234",
        "port": "6379",
        "encoding": "utf-8"
    }
    conn = redis.Redis(**REDIS_CONN_PARAMS)
    conn.hset("spider_result_dict", tid, value)


def run():
    while True:
        # 1. 获取任务
        task_json = get_task()
        print(task_json)
        if not task_json:
            continue

        # 将字符串解析为字典
        task_dict = json.loads(task_json)

        # 执行耗时操作
        ordered_string = task_dict['data']
        encrypt_string = ordered_string + "560c52ccd288fed045859ed18bffd973"
        obj = hashlib.md5(encrypt_string.encode('utf-8'))
        sign = obj.hexdigest()

        # 写入结果队列 (redis 的 hash)
        tid = task_dict['tid']
        set_result(tid, sign)

if __name__ == '__main__':
    run()