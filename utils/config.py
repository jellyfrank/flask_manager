
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

    def read(self, key):
        return self.cf.get(self.env, key)
