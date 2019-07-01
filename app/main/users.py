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
