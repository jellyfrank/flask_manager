
from app import db

# 通知人配置


class CfgNotify(db.Model):

    __routename__ = "notify"
    
    id = db.Column(db.Integer, primary_key=True)
    check_order = db.Column(db.Integer)  # 排序
    notify_type = db.Column(db.String)  # 通知类型：MAIL/SMS
    notify_name = db.Column(db.String)  # 通知人姓名
    notify_number = db.Column(db.String)  # 通知号码
    status = db.Column(db.Boolean, default=True)  # 生效失效标识
