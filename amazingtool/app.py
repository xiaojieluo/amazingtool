import tornado.ioloop
import tornado.web
from tornado.options import define, options
import tornado.wsgi

from api import route, settings

define("port", default="8888", help="listen port")

class Application(tornado.web.Application):
    def __init__(self):
        super(Application, self).__init__(handlers=route,**settings)

def make_app():
    # return tornado.web.Application(route, **settings)
    return Application()

# 使用 gunicorn 启动，速度大幅提升
# gunicorn --workers=4 app:app
wsgi_app = tornado.wsgi.WSGIApplication(route, **settings)


# wsgi_app = tornado.wsgi.WSGIAdapter(Application())
# server = wsgiref.simple_server.make_server('', 8888, wsgi_app)
# server.serve_forever()

if __name__ == '__main__':
    tornado.options.parse_command_line()
    app = make_app()
    app.listen(options.port)
    tornado.ioloop.IOLoop.current().start()
