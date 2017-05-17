import tornado.ioloop
import tornado.web
from tornado.options import define, options

from api import route, settings

define("port", default="8888", help="listen port")

class Application(tornado.web.Application):
    def __init__(self):
        super(Application, self).__init__(handlers=route,**settings)

def make_app():
    # return tornado.web.Application(route, **settings)
    return Application()

if __name__ == '__main__':
    tornado.options.parse_command_line()
    app = make_app()
    app.listen(options.port)
    tornado.ioloop.IOLoop.current().start()
