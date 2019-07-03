#!/usr/bin/python3
# @Time    : 2019-07-01
# @Author  : Kevin Kong (kfx2007@163.com)

from flask import request, flash, Response, redirect
from flask_login import login_required, current_user
from . import main
from utils.view_util import render_template
from .forms import UserPassword, MyForm
from utils.model_util import flash_errors
import qrcode
from autils import String
from autils.authentication import TwoStepVerification
from app import db
from io import BytesIO
from base64 import b64encode
import json


@main.route("/my", methods=["GET", "POST"])
@login_required
def my():
    """"个人中心"""
    if request.method == "GET":
        # 是否启用了二次验证
        context = {
            "form": MyForm(),
            "id": current_user.id,
            "enable": False
        }
        if current_user.enable_otp:
            img = qrcode.make(data=current_user.otp_str)
            buffer = BytesIO()
            img.save(buffer)
            img_stream = buffer.getvalue()
            # return Response(img_stream, content_type="image/png")
            image = b64encode(img_stream).decode("utf-8")
            image_url = f"data:image/png;base64,{image}"
            context["form"].enable.data = True
            context["image_url"] = image_url
        return render_template("my/my.html", **context)
    if request.method == "POST":
        fm = MyForm()
        id = int(request.json.get("id", None))
        state = bool(request.json.get("state", False))
        # 只允许修改自己的信息
        if id != current_user.id:
            flash("非法的操作")
            return render_template("my/my.html", form=fm, id=current_user.id)
        # 是否启用二次验证
        if state:
            tsv = TwoStepVerification(current_user.username)
            if not current_user.otp_str:
                # 生成二维码
                current_user.otp_str = tsv.otp_str
            current_user.enable_otp = True
            db.session.add(current_user)
            db.session.commit()
            img = qrcode.make(data=tsv.get_qrcode_string())
            buffer = BytesIO()
            img.save(buffer)
            img_stream = buffer.getvalue()
            # return Response(img_stream, content_type="image/png")
            image = b64encode(img_stream).decode("utf-8")
            image_url = f"data:image/png;base64,{image}"
            return json.dumps({"result": 0, "enable": True, "data": image_url})
            # return redirect("/my")
        else:
            # 停用二次验证
            fm.enable.data = False
            current_user.enable_otp = False
            db.session.add(current_user)
            db.session.commit()
        # return redirect("my/my.html", form=fm, id=current_user.id)
            return json.dumps({"result": 0, "enable": False})
