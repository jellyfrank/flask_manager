#!/usr/bin/python3
# @Time    : 2019-07-05
# @Author  : Kevin Kong (kfx2007@163.com)

from app import db


class Menu(db.Model):

    __routename__ = "menu"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)  # 菜单名称
    route = db.Column(db.String)  # 菜单路由
    parent = db.Column(db.Integer)  # 父级菜单
    model_name = db.Column(db.String)  # 模型名称
    active = db.Column(db.Boolean)  # 是否启用
    fields = db.Column(db.String)  # 列表字段
    type = db.Column(db.Integer) #菜单类型 1 列表， 2 编辑
