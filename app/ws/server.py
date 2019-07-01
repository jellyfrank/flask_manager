from tornado.websocket import WebSocketHandler
from app import logger, config
from .ssh import SSH
import threading
from app.model.servers import Server
import os
import asyncio


class SshHandler(WebSocketHandler):

    def check_origin(self, origin):
       return True

    # def initialize(self, *args,**kwargs):
    #     print('----')
    #     print(args, kwargs)

    def _reading(self):
        asyncio.set_event_loop(asyncio.new_event_loop())
        while True:
            data = self.ssh.read()
            self.write_message(data)

    def open(self, *args, **kwargs):
        logger.info("Websocket 打开")
        if args:
            server_id = int(args[0])
            server = Server.query.get(server_id)
            # if server.passwd:
            #     self.ssh = SSH(server.host, server.port,
            #                    server.user, server.passwd)
            # elif server.perm:
            #     keyfile = os.path.join(config.read("UPLOAD_PATH"), server.perm)
            #     self.ssh = SSH(server.ip, server.port,
            #                    server.user, keyfile=keyfile)
            if server.perm:
                keyfile = os.path.join(config.read("UPLOAD_PATH"), server.perm)
            else:
                keyfile = None
            self.ssh = SSH(server.ip, server.port,
                           server.user, server.passwd, keyfile, server.passcode)

            t = threading.Thread(target=self._reading)
            t.setDaemon(True)
            t.start()

    def on_message(self, message):
        if message.startswith("size"):
            cols, rows = message.split(':')[1].split(',')
            self.ssh.resize(int(cols), int(rows))
        else:
            self.ssh.send(message)

    def on_close(self):
        print("WebSocket Closed")
