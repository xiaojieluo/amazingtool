import tornado.web
# from amazingtool.db import database

from db import database

settings = dict(
    debug = True,
    siteurl = 'http://localhost:8888/',
    login_url = '/session',
    db = database().client,
)
