#!/usr/bin/python3
# @Time    : 2019-07-05
# @Author  : Kevin Kong (kfx2007@163.com)

from . import main
from flask_login import login_required
from flask import request
from utils.view_util import render_template
from app.model.menu import Menu
from app.main.forms import MenuForm

@main.route("/settings", methods=["GET", "POST"])
@login_required
def settings():
    pass


