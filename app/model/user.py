
from app import db
from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import UserMixin
from app import login_manager


class User(UserMixin, db.Model):

    # __routename__ = "user"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String)  # 用户名
    password = db.Column(db.String)  # 密码
    fullname = db.Column(db.String)  # 真实性名
    email = db.Column(db.String)  # 邮箱
    phone = db.Column(db.String)  # 电话
    status = db.Column(db.Boolean, default=True)  # 状态
    enable_otp = db.Column(db.Boolean, default=False)  # 是否启用二次验证
    otp_str = db.Column(db.String)  # 二次验证密钥

    def verify_password(self, raw_password):
        return check_password_hash(self.password, raw_password)

    def update_password(self, raw_password):
        """更新密码"""
        self.password = generate_password_hash(raw_password)
        db.session.add(self)
        db.session.commit()


@login_manager.user_loader
def load_user(user_id):
    return User.query.filter(User.id == int(user_id)).first()
