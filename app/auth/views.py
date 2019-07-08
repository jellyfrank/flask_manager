from flask import render_template, redirect, request, url_for, flash
from . import auth
from .forms import LoginForm
from app.model.user import User
from flask_login import login_user, logout_user, login_required
from app import logger
import traceback
from autils.authentication import TwoStepVerification
from app.main.views import register_comm_menus


@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        try:
            user = User.query.filter(
                User.username == form.username.data).first()
            # 二次验证
            if user.enable_otp:
                if not form.otp_code.data:
                    form.enable_otp.data = True
                    flash("用户开启了二次验证，请输入验证码")
                    return render_template('auth/login.html', form=form)
                # 验证二次验证
                tsv = TwoStepVerification(user.username)
                if not tsv.check(user.otp_str, form.otp_code.data):
                    form.enable_otp.data = True
                    flash("二次验证失败")
                    return render_template('auth/login.html', form=form)

            if user:
                if user.verify_password(form.password.data):
                    # 获取菜单
                    register_comm_menus()
                    login_user(user, form.rememberme.data)
                    return redirect(request.args.get('next') or url_for('main.index'))
                else:
                    flash("用户名或密码错误")
            else:
                flash('用户不存在')
        except Exception as ex:
            logger.error("ex:{}".format(traceback.format_exc()))
            flash('用户名或密码错误')
    return render_template('auth/login.html', form=form)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('您已退出登录')
    return redirect(url_for('auth.login'))
