#!/usr/bin/python3
# @Time    : 2019-07-01
# @Author  : Kevin Kong (kfx2007@163.com)

from flask import render_template as rt
from app import config
from app.model.menu import Menu


def get_menus():
    # 获取通用菜单
    # 获取顶级菜单
    data = []
    menus = Menu.query.filter(Menu.active == True, Menu.parent == 0).all()
    for menu in menus:
        childs = Menu.query.filter(
            Menu.active == True, Menu.parent == menu.id).all()
        data.append({
            "name": menu.name,
            "route": f"main.{menu.route}" if menu.route else None,
            "icon": menu.icon,
            "childs": [{
                "name": child.name,
                "route": f"main.{child.model_name}{'list' if child.type==1 else 'edit'}",
                "icon": child.icon
            } for child in childs]
        })
    return data


def render_template(template, **context):
    """添加常量"""
    for key, value in config.comm.items():
        context[key] = value
        context["menus"] = get_menus()
    return rt(template, **context)
