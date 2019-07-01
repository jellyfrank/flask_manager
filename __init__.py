from app import app, config

# if __name__ == "__main__":
#     app.run(host=config.read("HOST"), port=int(config.read(
#         "PORT")), debug=config.read("DEBUG"))

from tornado.web import FallbackHandler, Application, StaticFileHandler
from tornado.wsgi import WSGIContainer
from tornado.ioloop import IOLoop
from app.ws.server import SshHandler
from tornado.httpserver import HTTPServer
import ssl
import os

app = WSGIContainer(app)
# term_manager = SingleTermManager(shell_command=['bash'])
# print('11')
# print(term_manager.extra_env)
handlers = [
    (r"/websocket/(.*)", SshHandler,{}),# {'term_manager': term_manager}),
    # (r"/ssh", StaticFileHandler, {'path': 'index.html'}),
    # (r"/(.*)", tornado.web.StaticFileHandler, {'path': '.'}),
    (r"/(.*)", FallbackHandler, dict(fallback=app))
]

application = Application(handlers,debug=True)

# application.listen(5000)

if __name__ == "__main__":    
    sp = config.read("secure_path")
    if sp:
        # ssl_ctx = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
        # ssl_ctx.load_cert_chain(os.path.join(config.read("secure_path"), "mydomain.crt"),
        #                     os.path.join(config.read("secure_path"), "mydomain.key"))
        httpserver = HTTPServer(application,ssl_options={
            "certfile": os.path.join(config.read("secure_path"), "1_home.mixoo.cn_bundle.crt"),
            "keyfile":  os.path.join(config.read("secure_path"), "2_home.mixoo.cn.key"),
        })
    else:
        httpserver = HTTPServer(application)
    httpserver.listen(int(config.read("PORT")))
    IOLoop.current().start()