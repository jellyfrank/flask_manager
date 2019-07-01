from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField, PasswordField, SelectField, TextAreaField, HiddenField, FileField
from wtforms import IntegerField, DateTimeField
from wtforms.validators import DataRequired, Length, Email, Regexp, EqualTo


class CfgNotifyForm(FlaskForm):

    __routename__ = "notify"

    check_order = StringField('排序', validators=[DataRequired(
        message='不能为空'), Length(0, 64, message='长度不正确')])
    notify_type = SelectField('通知类型', choices=[('MAIL', '邮件通知'), ('SMS', '短信通知')],
                              validators=[DataRequired(message='不能为空'), Length(0, 64, message='长度不正确')])
    notify_name = StringField('通知人姓名', validators=[DataRequired(
        message='不能为空'), Length(0, 64, message='长度不正确')])
    notify_number = StringField('通知号码', validators=[DataRequired(
        message='不能为空'), Length(0, 64, message='长度不正确')])
    status = BooleanField('生效标识', default=True)
    submit = SubmitField('提交')


class ServerForm(FlaskForm):

    __routename__ = "server"

    name = StringField('名称', validators=[DataRequired(
        message='不能为空'), Length(0, 64, message="长度不正确")])
    ip = StringField('IP地址', validators=[DataRequired(
        message='不能为空'), Length(0, 64, message="长度不正确")])
    port = StringField('端口号', validators=[DataRequired(
        message='不能为空'), Length(0, 64, message="长度不正确")])
    user = StringField('用户名', validators=[DataRequired(
        message='不能为空'), Length(0, 64, message="长度不正确")])
    passwd = PasswordField('密码')
    perm = FileField("密钥文件")
    passcode = PasswordField('秘钥密码')
    submit = SubmitField("提交")


class UserPassword(FlaskForm):

    old_password = PasswordField("旧密码", validators=[DataRequired(
        message="不能为空"
    )])
    new_password = PasswordField("新密码", validators=[
        DataRequired(message="不能为空"),
        EqualTo('verify_password', message='两次密码不一致')])
    verify_password = PasswordField("再次输入新密码", [DataRequired(message="不能为空")])
    submit = SubmitField("修改密码")
