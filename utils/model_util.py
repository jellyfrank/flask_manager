from app import db
from flask import flash
from sqlalchemy.inspection import inspect


def get_model_colums_dict(Model):
    res =  {m.key: getattr(Model, m.key) for m in Model.__table__.columns}
    for rel in inspect(Model).mapper.relationships:
        key = str(rel).split('.')[1].lower()
        res[key] = getattr(Model,key)
    return res


def flash_errors(form):
    for field, errors in form.errors.items():
        for error in errors:
            flash("字段 [%s] 格式有误,错误原因: %s" % (
                getattr(form, field).label.text,
                error
            ))
