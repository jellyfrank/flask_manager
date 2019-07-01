

import paramiko
from app import logger


class SSH(object):

    def __init__(self, host, port, user, password=None, keyfile=None, passphrase=None):
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.keyfile = keyfile
        self._ssh = paramiko.SSHClient()
        self._ssh.load_system_host_keys()
        self._ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        # if self.password:
        #     self._ssh.connect(host, port, user, password)
        # elif self.keyfile:
        #     k = paramiko.RSAKey.from_private_key_file(keyfile)
        #     self._ssh.connect(hostname=host, port=port,
        #                       username=user, pkey=k)
        k = keyfile and paramiko.RSAKey.from_private_key_file(
            keyfile, password=passphrase) or None
        self._ssh.connect(hostname=host, port=port, username=user,
                          password=password, pkey=k)
        self._chanel = self._ssh.invoke_shell(
            term='xterm')
        # self._chanel.setblocking(0)
        # self._chanel.resize_pty(width=50, height=70)

    def resize(self, cols, rows):
        logger.info("重置窗口大小:{},{}".format(cols, rows))
        self._chanel.resize_pty(width=cols, height=rows)

    def send(self, msg):
        self._chanel.send(msg)

    def read(self):
        return self._chanel.recv(10000)
