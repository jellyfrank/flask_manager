#!/usr/bin/python3
# @Time    : 2019-07-01
# @Author  : Kevin Kong (kfx2007@163.com)

from flask import request, flash
from flask_login import login_required, current_user
from . import main
from utils.view_util import render_template
from .forms import UserPassword
from utils.model_util import flash_errors


@main.route("/my", methods=["GET", "POST"])
@login_required
def my():
    """"个人中心"""
    if request.method == "GET":
        return render_template("my/my.html")
