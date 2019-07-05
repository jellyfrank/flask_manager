#!/usr/bin/python3
# @Time    : 2019-07-05
# @Author  : Kevin Kong (kfx2007@163.com)

from . import main
from flask_login import login_required, current_user
from utils.view_util import render_template
from flask import redirect, url_for, request
from app.model.menu import Menu

# 根目录跳转
@main.route('/', methods=['GET'])
@login_required
def root():
    return redirect(url_for('main.index'))


# 首页
@main.route('/index', methods=['GET'])
@login_required
def index():
    # 获取通用菜单
    # 获取顶级菜单
    # data = {}
    # menus = Menu.query.filter(Menu.active == True, Menu.parent == 0).all()
    # for menu in menus:
    #     data["name"] = menu.name
    #     childs = Menu.query.filter(
    #         Menu.active == True, Menu.parent == menu.id).all()
    #     data["childs"] = [{"name"}]

    return render_template('index.html', current_user=current_user, menus=menus)


@main.route('/term')
@login_required
def get_term():
    id = request.args.get("id")
    return render_template("term.html", server_id=id)
