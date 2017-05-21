#!/usr/bin/env python
# coding=utf-8

import json
from tornado.web import Finish
import tornado.web

import sys
sys.path.append('../')
from amazingtool.db import db

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

        # self.write(json.dumps({
        #     'meta':status_code,
        #     'data':data,
        #     'msg':msg,
        # }))
        self.write(json.dumps(data))
        raise Finish()

    def write_error(self, data, status_code=404, msg='error.'):
        self.write_json(data, status_code, msg)
