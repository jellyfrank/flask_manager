from app import app, config, logger
from tornado.web import FallbackHandler, Application, StaticFileHandler
from tornado.wsgi import WSGIContainer
from tornado.ioloop import IOLoop
from app.ws.server import SshHandler
from tornado.httpserver import HTTPServer
import ssl
import os

app = WSGIContainer(app)
handlers = [
    (r"/websocket/(.*)", SshHandler, {}),  # {'term_manager': term_manager}),
    (r"/(.*)", FallbackHandler, dict(fallback=app))
]

application = Application(handlers, debug=True)

if __name__ == "__main__":
    sp = config.secure_path
    if sp:
        httpserver = HTTPServer(application, ssl_options={
            "certfile": os.path.join(config.secure_path, config.certfile_path),
            "keyfile":  os.path.join(config.secure_path, config.key_path),
        })
    else:
        httpserver = HTTPServer(application)
    httpserver.listen(int(config.PORT))
    logger.info(f"服务器[{config.HOST}]在端口[{config.PORT}]已启动监听, 数据库服务器地址:[{config.DB_HOST}]")
    IOLoop.current().start()
