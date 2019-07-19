from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField, PasswordField, SelectField, TextAreaField, HiddenField, FileField
from wtforms import IntegerField, DateTimeField
from wtforms.validators import DataRequired, Length, Email, Regexp, EqualTo
from app.model.group import Permission


class MenuForm(FlaskForm):

    __routename__ = "menu"

    name = StringField("菜单名称", validators=[DataRequired(
        message='不能为空'), Length(0, 64, message='长度不正确')])
    route = StringField("菜单路由")
    parent = IntegerField("父级菜单", default=0)
    model_name = StringField("模型名称")
    # fields = StringField("列表视图字段")
    active = BooleanField("是否启用", default=False)
    type = SelectField("类型", choices=[('1', "列表"),
                                      ('2', "编辑")
                                      ])
    icon = StringField("菜单图标")
    submit = SubmitField('提交')


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


class Users(FlaskForm):

    username = StringField("用户名", validators=[DataRequired("用户名不能为空")])
    password = PasswordField("密码", validators=[DataRequired("密码不能为空")])
    fullname = StringField("姓名")
    email = StringField("邮箱", validators=[DataRequired("邮箱必填")])
    phone = StringField("电话")
    status = BooleanField("启用")
    enable_otp = BooleanField("是否启用两步验证")
    submit = SubmitField("提交")


class MyForm(FlaskForm):

    uid = IntegerField("用户id")
    otp_str = StringField("请使用二次验证APP(Google Authenticator)扫码，并妥善保管您的二维码。")
    enable = BooleanField("是否启用二次验证登录", default=False)
    submit = SubmitField("生成")


class GroupForm(FlaskForm):

    name = StringField("角色名称")
    parent_id = IntegerField("父级角色")
    permissions = SelectField("权限",coerce=int)
    submit = SubmitField("提交")

class PermissionForm(FlaskForm):

    name = StringField("权限名称")
    submit = SubmitField("提交")



