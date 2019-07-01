from app import db
from flask import flash


def get_model_colums_dict(Model):
    return {m.key: getattr(Model, m.key) for m in Model.__table__.columns}


def flash_errors(form):
    for field, errors in form.errors.items():
        for error in errors:
            flash("字段 [%s] 格式有误,错误原因: %s" % (
                getattr(form, field).label.text,
                error
            ))
