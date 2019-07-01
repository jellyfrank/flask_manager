
from configparser import ConfigParser


class Config(object):

    def __init__(self, path, env):
        '''
        读取配置文件
        path: 配置文件 路径
        '''

        self.cf = ConfigParser()
        self.cf.read(path)
        self.env = env
        self.comm = dict()
        self._set_comm_variants()

    def __getattr__(self, key):
        return self.cf.get(self.env, key)

    def _set_comm_variants(self):
        for key, value in self.cf._sections["COMM"].items():
            self.comm[key] = value
