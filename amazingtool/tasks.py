from celery import Celery
import requests
import json
import time

# from amazingtool.db import database
from db import database
from api.web import Cache
# from amazingtool.api.settings import settings

broker = 'redis://localhost:6379/1'
# broker = 'amqp://xiaojieluo:041000lxj@ArchLinux:5672/amazingtool_vhost'
backend = 'redis://localhost:6379/2'
# backend = ''

app = Celery('AmazingTool', broker = broker, backend = backend)
db = database().client
cache = Cache().r

@app.task(bind=True)
def ip(self, ip):
    url = 'http://ip-api.com/json/'
    r = requests.get(url+ip)
    print(r.text)
    return json.loads(r.text)

@app.task(ignore_result=True)
def update(type_, data):
    '''
    当数据不存在时,更新 mongodb 数据库
        type_ : 加密类型
        data  : 源数据与加密后的数据, dict 格式,
            { text:'', result:'' }
    '''
    import time
    time.sleep(1)
    database = db[type_]
    if database.find_one(data) is None:
        database.insert_one(data)

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
