# from app import get_logger, get_config
from app import model, app, main
from app import logger, config
from app.main.forms import *
import math
from flask import redirect, url_for, flash, request, abort
from utils.view_util import render_template
from flask_login import login_required, current_user
# from app import utils
from . import bp_main
from utils import model_util
from app import db
import inspect
from flask_wtf import FlaskForm
import os
from app.model.servers import Server
from app.model.menu import Menu
from app.model.user import User
import traceback
from sqlalchemy.inspection import inspect as isp


# 通用列表查询


def common_list(DynamicModel, view, pk="id", **context):
    # 接收参数
    action = request.args.get('action')
    id = request.args.get('id')
    page = int(request.args.get('page')) if request.args.get('page') else 1
    length = int(request.args.get('length') if request.args.get(
        'length') else config.ITEMS_PER_PAGE)

    # 删除操作
    if action == 'del' and id:
        try:
            m = DynamicModel.query.get(id)
            db.session.delete(m)
            db.session.commit()
            flash('删除成功')
        except Exception as ex:
            logger.error("删除异常:{}".format(ex))
            flash('删除失败')

    # 查询列表
    result = DynamicModel.query.order_by(
        getattr(DynamicModel, pk)).paginate(page, length, False)
    dict = {'content': [model_util.get_model_colums_dict(item) for item in result.items],
            'total_page': math.ceil(result.total / length), 'page': page, 'length': length}
    return render_template(view, form=dict, current_user=current_user, **context)


# 通用单模型查询&新增&修改
def common_edit(DynamicModel, form, view, pk="id", ** context):
    try:
        id = request.args.get(pk, '')
        if id:
            # 查询
            model = DynamicModel.query.get(id)
            if model:
                if request.method == 'GET':
                    dict = model_util.get_model_colums_dict(model)
                    for key, value in dict.items():
                        if key in form.__dict__ and value:
                            field = getattr(form, key)
                            field.data = dict.get(key)
                            setattr(form, key, field)
                # 修改
                if request.method == 'POST':
                    if form.validate_on_submit():
                        for field in form:
                            if field.type == 'FileField':
                                file = request.files[field.name]
                                if file.filename:
                                    file.save(os.path.join(config.read(
                                        "UPLOAD_PATH"), file.filename))
                                    setattr(model, field.name, file.filename)
                            elif field.type == 'BooleanField':
                                setattr(model, field.name, bool(field.data))
                            else:
                                setattr(model, field.name, field.data)
                        db.session.add(model)
                        db.session.commit()
                        flash('修改成功')
                    else:
                        model_util.flash_errors(form)
        else:
            # 新增
            if form.validate_on_submit():
                dict = model_util.get_model_colums_dict(DynamicModel)
                conditions = []
                for field in form:
                    if field.name in dict.keys():
                        if field.type == "FileField":
                            file = request.files.get(field.name, None)
                            if file and file.filename:
                                file.save(os.path.join(config.read(
                                    "UPLOAD_PATH"), file.filename))
                                conditions.append("{}='{}'".format(
                                    field.name, file.filename))
                        elif field.type == 'BooleanField':
                            conditions.append(
                                f"{field.name}={field.data}"
                            )
                        else:
                            conditions.append(
                                "{}='{}'".format(field.name, field.data))
                fields = ",".join(conditions)
                # [FIXME] eval should not use
                m = eval("{}({})".format(
                    DynamicModel.__name__, fields), None, None)
                db.session.add(m)
                db.session.commit()
                flash('保存成功')
            else:
                model_util.flash_errors(form)
    except Exception as err:
        logger.error(f"通用模型添加或修改异常:{traceback.format_exc()}")
    return render_template(view, form=form, current_user=current_user, **context)


# 自动路由
model_class = {
    hasattr(v, "__routename__") and v.__routename__ or k: v 
    for key, value in inspect.getmembers(model) 
    if inspect.ismodule(
        value) for k, v in inspect.getmembers(value) if inspect.isclass(v)
    and issubclass(v, db.Model) and getattr(v, "__routename__", False)
}

form_class = {
    hasattr(v, "__routename__") and v.__routename__ or k: v 
    for key, value in inspect.getmembers(main) if inspect.ismodule(
        value) for k, v in inspect.getmembers(value) if inspect.isclass(v)
    and issubclass(v, FlaskForm) and getattr(v, "__routename__", False)
}

logger.debug(f"已注册的模型:{model_class}")
#[FIXME] form_class结果为空
logger.debug(f"已注册的表单:{form_class}")


def register_route(url, methods, func, login=True):
    '''注册路由'''
    logger.info(f"注册路由:{url},endpoint:{methods},func:{func.__name__}")
    if login:
        bp_main.route(url, methods=methods)(login_required(func))
    else:
        bp_main.route(url, methods=methods)(func)


@bp_main.route("/comm/<route>", methods=["GET", "POST"])
@login_required
def comm_action(route):
    menu = Menu.query.filter(
        Menu.active == True, Menu.route == route).first()
    if not menu:
        abort(404)
    if request.method == "GET":
        if menu.type == 1:
            me = Menu.query.filter(
                Menu.active == True, Menu.model_name == menu.model_name, Menu.type == "2").first()
            pk = isp(model_class.get(menu.model_name)).primary_key[0].name
            fm = form_class.get(menu.model_name,None)
            if not fm:
                raise Exception(f"不存在与{menu.model_name}对应的表单，是否定义了？")
            
            return common_list(model_class.get(menu.model_name), "menu/commlist.html", nav=menu.name, pk=pk, editroute=f"{me.route}" if me else None, fm=fm())
        if menu.type == 2:
            return common_edit(model_class.get(menu.model_name), form_class.get(menu.model_name)(), "menu/commedit.html", nav=menu.name)
    if request.method == "POST":
        return common_edit(model_class.get(menu.model_name), form_class.get(menu.model_name)(), "menu/commedit.html", nav=menu.name)
