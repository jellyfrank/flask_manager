#!/usr/bin/python3
# @Time    : 2019-07-01
# @Author  : Kevin Kong (kfx2007@163.com)

# 用户安全相关
from flask import request, flash
from flask_login import login_required, current_user
from . import main
from utils.view_util import render_template
from .forms import UserPassword
from utils.model_util import flash_errors
from app.model.user import User
from app.main.forms import Users
from app.main.views import common_list, common_edit
from werkzeug.security import generate_password_hash


@main.route("/changepasswd", methods=["GET", "POST"])
@login_required
def changepasswd():
    """修改密码"""
    if request.method == "GET":
        return render_template("user/changepasswd.html", form=UserPassword())
    if request.method == "POST":
        # 验证输入的密码是否符合条件
        form = UserPassword(request.form)
        old_password = request.form.get("old_password")
        new_password = request.form.get("new_password")
        if not form.validate_on_submit():
            flash_errors(form)
            return render_template("user/changepasswd.html", form=form)
        # 验证原密码是否正确
        if not current_user.verify_password(old_password):
            flash("原密码不正确")
            return render_template("user/changepasswd.html", form=form)
        # 更新密码
        current_user.update_password(new_password)
        flash("密码修改成功")
        return render_template("user/changepasswd.html", form=form)


@main.route("/userlist", methods=["GET"])
@login_required
def userlist():
    """用户管理"""
    users = User.query.all()
    form = Users()
    return common_list(User, "user/userlist.html")


@main.route("/useredit", methods=["GET", "POST"])
@login_required
def useredit():
    """用户编辑"""
    form = Users()
    if request.method == "POST":
        if "password" in request.form:
            form.password.data  = generate_password_hash(request.form["password"])
    return common_edit(User,form,"user/useredit.html")
