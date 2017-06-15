import tornado.ioloop
import tornado.web
from tornado.options import define, options
import tornado.wsgi

from api import route
from settings import settings

define("port", default="8888", help="listen port")

class Application(tornado.web.Application):
    def __init__(self):
        super(Application, self).__init__(handlers=route,**settings)

def make_app():
    return Application()

# gunicorn --workers=4 app:app
app = tornado.wsgi.WSGIApplication(route, **settings)


if __name__ == '__main__':
    tornado.options.parse_command_line()
    app = make_app()
    app.listen(options.port)
    tornado.ioloop.IOLoop.current().start()
