from celery import Celery
import requests
import json
import time

from db import db

broker = 'redis://localhost:6379'
backend = 'redis://localhost:6379'

app = Celery('AmazingTool', broker = broker, backend = backend)

@app.task(bind=True)
def log(self, data):
    '''
    日志记录,持久化存储
    所有写日志操作都放到 celery 队列中异步执行,不阻塞主程序
    '''
    log_db = db['amazingtool_log']

    try:
        log_db.insert_one(data)
    except Exception as e:
        raise self.retry(exc=e, countdown=5, max_retries=6)
#
#
# def update(type_, query, data):
#     '''
#     当数据不存在时,更新 mongodb 数据库
#         type_ : 类型
#         data  : 要写入数据库的内容, dict 格式,
#             { text:'', result:'' }
#     '''
#     database = db[type_]
#     if isinstance(data, str):
#         data = json.loads(data)
#
#     # print(query)
#
#     if database.find_one(query) is None:
#         database.insert_one(data)
#
#     return data
