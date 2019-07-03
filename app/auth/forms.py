from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Length


class LoginForm(FlaskForm):
    username = StringField('用户名', validators=[DataRequired(), Length(1, 64), ])
    password = PasswordField('密码', validators=[DataRequired()])
    enable_otp = StringField("是否开启二次验证", default=False)
    otp_code = StringField("二次验证码")
    rememberme = BooleanField('记住我')
    submit = SubmitField('提交')
