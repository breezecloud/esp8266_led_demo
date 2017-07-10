import tornado.web
import tornado.httpserver
import tornado.ioloop
import tornado.options
from uuid import uuid4



class DetailHandler(tornado.web.RequestHandler):
    def get(self):
        session = uuid4()
        self.render("index.html", session=session)

class Application(tornado.web.Application):
    def __init__(self):

        handlers = [
            (r'/', DetailHandler),
        ]

        settings = {
            'template_path': 'templates',
            'static_path': 'static'
        }

        tornado.web.Application.__init__(self, handlers, **settings)

if __name__ == '__main__':
    tornado.options.parse_command_line()

    app = Application()
    server = tornado.httpserver.HTTPServer(app)
    server.listen(8000)
    tornado.ioloop.IOLoop.instance().start()