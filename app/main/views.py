# from app import get_logger, get_config
from app import model, app
from app import logger, config
import math
from flask import redirect, url_for, flash, request, abort
from utils.view_util import render_template
from flask_login import login_required, current_user
# from app import utils
from app.main import forms
from . import main
from utils import model_util
from app import db
import inspect
from flask_wtf import FlaskForm
import os
from app.model.servers import Server
from app.model.menu import Menu
from app.model.user import User
import traceback

# 通用列表查询


def common_list(DynamicModel, view, **context):
    # 接收参数
    # logger.debug("---------")
    # for rule in app.url_map.iter_rules():
    #     logger.debug(f"当前路由表：{rule}")
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
        DynamicModel.id).paginate(page, length, False)
    dict = {'content': [model_util.get_model_colums_dict(item) for item in result.items],
            'total_page': math.ceil(result.total / length), 'page': page, 'length': length}
    return render_template(view, form=dict, current_user=current_user, **context)


# 通用单模型查询&新增&修改
def common_edit(DynamicModel, form, view, **context):
    id = request.args.get('id', '')
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
                        file = request.files.get(field.name,None)
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
            m = eval("{}({})".format(DynamicModel.__name__, fields), None, None)
            db.session.add(m)
            db.session.commit()
            flash('保存成功')
        else:
            model_util.flash_errors(form)
    return render_template(view, form=form, current_user=current_user, **context)


# 自动路由
model_class = {
    hasattr(v, "__routename__") and v.__routename__ or k: v for key, value in inspect.getmembers(model) if inspect.ismodule(
        value) for k, v in inspect.getmembers(value) if inspect.isclass(v)
    and issubclass(v, db.Model) and getattr(v, "__routename__", False)
}

form_class = {
    hasattr(value, "__routename__") and value.__routename__ or key: value
    for key, value in inspect.getmembers(forms) if inspect.isclass(value)
    and issubclass(value, FlaskForm) and getattr(value, "__routename__", False)
}


def register_route(url, methods, func, login=True):
    '''注册路由'''
    logger.info(f"注册路由:{url},endpoint:{methods},func:{func.__name__}")
    if login:
        main.route(url, methods=methods)(login_required(func))
    else:
        main.route(url, methods=methods)(func)


# for name, cls in model_class.items():

#     list_method, edit_method = "{}list".format(
#         cls.__routename__), "{}edit".format(cls.__routename__)

#     def func_list():
#         ns, ep = request.url_rule.endpoint.split('.')
#         pre = ep.split('list')[0]
#         return common_list(model_class.get(pre), f'{pre}/{ep}.html')
#     func_list.__name__ = list_method
#     register_route("/{}".format(list_method),
#                    ["GET", "POST"], func_list)

#     def func_eidt():
#         ns, ep = request.url_rule.endpoint.split('.')
#         pre = ep.split('edit')[0]
#         return common_edit(model_class.get(pre), form_class.get(pre)(), f'{pre}/{ep}.html')
#     func_eidt.__name__ = edit_method
#     register_route("/{}".format(edit_method), ["GET", "POST"], func_eidt)

# 通用菜单注册
# def register_comm_menus():
#     # 菜单数据异常则跳过不加载
#     try:
#         menus = Menu.query.filter(Menu.active == True).all()
#     except Exception as err:
#         logger.error(f"通用菜单加载异常:{traceback.format_exc()}")
#         return
#     for menu in menus:
#         if menu.route:
#             # 注册列表路由
#             if menu.type == 1:
#                 # 查找是否存在对应的编辑路由
#                 me = Menu.query.filter(Menu.active == True, Menu.model_name==menu.model_name,Menu.type=="2").first()
#                 comm_menu_list = lambda m=menu: common_list(model_class.get(m.model_name), "menu/commlist.html", nav=m.name, editroute=f"main.{me.model_name}edit" if me else None, fm=form_class.get(m.model_name)())
#                 comm_menu_list.__name__ = f"{menu.model_name}list"
#                 register_route(f"{menu.route}", ["GET"], comm_menu_list)
#             # 注册编辑路由
#             if menu.type == 2:
#                 comm_menu_edit = lambda m=menu: common_edit(model_class.get(m.model_name), form_class.get(m.model_name)(),"menu/commedit.html", nav=m.name)
#                 comm_menu_edit.__name__ = f"{menu.model_name}edit"
#                 register_route(f"{menu.route}",["GET","POST"],comm_menu_edit)


@main.route("/comm/<route>", methods=["GET", "POST"])
@login_required
def comm_action(route):
    try:
        menu = Menu.query.filter(Menu.active == True, Menu.route == route).first()
        if not menu:
            abort(404)
        if request.method == "GET":
            if menu.type == 1:
                me = Menu.query.filter(
                    Menu.active == True, Menu.model_name == menu.model_name, Menu.type == "2").first()
                return common_list(model_class.get(menu.model_name), "menu/commlist.html", nav=menu.name, editroute=f"{me.route}" if me else None, fm=form_class.get(menu.model_name)())
            if menu.type == 2:
                return common_edit(model_class.get(menu.model_name), form_class.get(menu.model_name)(), "menu/commedit.html", nav=menu.name)
        if request.method == "POST":
            return common_edit(model_class.get(menu.model_name), form_class.get(menu.model_name)(), "menu/commedit.html", nav=menu.name)
    except Exception as err:
        logger.error(f"通用路由响应异常:{traceback.format_exc()}")
