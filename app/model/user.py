
from app import db
from werkzeug.security import check_password_hash
from flask_login import UserMixin
from app import login_manager


class User(UserMixin,db.Model):

    # __routename__ = "user"

    id = db.Column(db.Integer,primary_key=True)
    username  = db.Column(db.String)  # 用户名
    password  = db.Column(db.String)  # 密码
    fullname  = db.Column(db.String)  # 真实性名
    email  = db.Column(db.String)  # 邮箱
    phone  = db.Column(db.String)  # 电话
    status = db.Column(db.Boolean,default=True) # 状态

    def verify_password(self, raw_password):
        return check_password_hash(self.password, raw_password)


@login_manager.user_loader
def load_user(user_id):
    return User.query.filter(User.id == int(user_id)).first()