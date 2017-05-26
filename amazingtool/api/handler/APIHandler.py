import json
from tornado.web import Finish
import tornado.web

import sys
sys.path.append('../')
from amazingtool.db import db
import time
import tasks

class APIHandler(tornado.web.RequestHandler):

    def __init__(self, application, request, **kwargs):
        super().__init__(application, request, **kwargs)
        self.set_header('Content-Type', 'text/json')
        self.set_header('Server', 'You guess.')
        self.set_header('Connection','keep-alive')
        self.set_header('Access-Control-Allow-Origin','*')

        if self.settings.get('allow_remote_access'):
            self.access_control_allow()
        self.db = db

    def language(self, lang = 'en'):
        '''
        api 的多语言支持
        '''
        # lang = self.get_argument('lang', 'en')
        pass

    def site_url(self, url):
        '''
        构造 api 地址
        '''
        return self.settings.get('siteurl') + url

    def write_json(self, data, status_code=200, msg='success.'):
        self.set_header('Cache-Control', "no-cache")
        self.set_status(status_code)
        self.write(json.dumps(data))
        raise Finish()

    def write_error(self, msg='error.', status_code=404):
        data = dict(
            code=status_code,
            msg=msg
        )
        self.write_json(data, status_code)

    def log(self, msg, name='AmazingTool', level='info'):
        '''
        日志记录
        将程序产生的日志信息进行记录并持久化存储
        '''
        data = dict(
            name = 'celery',
            level = level,
            datetime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()),
            msg = msg
        )

        # log_db.insert_one(data)
        try:
            tasks.log.delay(data)
        except:
            print("Error.....celery not start")

        # print(log_db)
