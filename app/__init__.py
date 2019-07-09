

from utils.config import Config
from autils import Logger
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from autils import String
import logging
# from flask_apscheduler import APScheduler

login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'auth.login'

config = Config("config.ini", "DEV")
logger = Logger(config.log,level=logging.DEBUG if config.DEBUG else logging.INFO).logger

app = Flask(__name__)
login_manager.init_app(app)
app.config['SECRET_KEY'] = String.generate()
app.config["SQLALCHEMY_DATABASE_URI"] = config.DB_URL.format(
    user=config.DB_USER,
    password=config.DB_PWD,
    url=config.DB_HOST,
    port=int(config.DB_PORT),
    db=config.DB_NAME
)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True

db = SQLAlchemy(app)

from .auth import auth
from .main import main

app.register_blueprint(auth)
app.register_blueprint(main)

# scheduler = APScheduler()
# scheduler.init_app(app)
# scheduler.start()
