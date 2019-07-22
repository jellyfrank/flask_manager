#!/usr/bin/python3
# @Time    : 2019-07-01
# @Author  : Kevin Kong (kfx2007@163.com)

# 用户安全相关
from flask import request, flash
from flask_login import login_required, current_user
from . import bp_main
from utils.view_util import render_template
from utils.model_util import flash_errors
from app.model.group import Group, Permission
from app.main.forms import GroupForm, PermissionForm
from app.main.views import common_list, common_edit
from werkzeug.security import generate_password_hash

@bp_main.route("/grouplist", methods=["GET"])
@login_required
def grouplist():
    """组管理"""
    return common_list(Group, "group/grouplist.html")


@bp_main.route("/groupedit", methods=["GET", "POST"])
@login_required
def groupedit():
    """用户编辑"""
    form = GroupForm()
    if request.method == "POST":
        form = GroupForm(request.form)
        if "password" in request.form:
            form.password.data  = generate_password_hash(request.form["password"])
    form.permissions.choices = [(p.id,p.name) for p in Permission.query.order_by("id")]
    return common_edit(Group,form,"group/groupedit.html")

@bp_main.route("/permissionlist", methods=["GET"])
@login_required
def permissionlist():
    """权限管理"""
    return common_list(Permission, "group/permissionlist.html")


@bp_main.route("/permissionedit", methods=["GET", "POST"])
@login_required
def permissionedit():
    """权限编辑"""
    form = PermissionForm()
    if request.method == "POST":
        if "password" in request.form:
            form.password.data  = generate_password_hash(request.form["password"])
    return common_edit(Permission,form,"group/permissionedit.html")
