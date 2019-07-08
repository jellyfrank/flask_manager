

from flask import Blueprint

main = Blueprint('main', __name__)

from . import index
from . import views, forms, errors
from . import users
from . import my
from . import settings

