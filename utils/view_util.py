#!/usr/bin/python3
# @Time    : 2019-07-01
# @Author  : Kevin Kong (kfx2007@163.com)

from flask import render_template as rt
from app import config


def render_template(template, **context):
    """添加常量"""
    for key, value in config.comm.items():
        context[key] = value
    return rt(template, **context)
