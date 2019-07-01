
from app import db

class Server(db.Model):

    __routename__ = "server"

    id  = db.Column(db.Integer,primary_key=True)
    name  = db.Column(db.String) #名称
    ip  = db.Column(db.String) #IP地址
    port  = db.Column(db.String) #端口号
    user = db.Column(db.String) #用户
    passwd  = db.Column(db.String) #密码
    perm = db.Column(db.String) #秘钥文件名称
    passcode = db.Column(db.String) #秘钥密码
