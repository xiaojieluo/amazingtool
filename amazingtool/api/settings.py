#!/usr/bin/env python
# coding=utf-8

import tornado.web
from amazingtool.db import database

settings = dict(
    debug = True,
    siteurl = 'http://localhost:8888/',
    login_url = '/session',
    db = database().client,
)
