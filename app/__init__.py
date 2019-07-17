#!/usr/bin/python3
# @Time    : 2019-07-16
# @Author  : Kevin Kong (kfx2007@163.com)

from utils.config import Config
from autils import Logger
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from autils import String
import logging

login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'auth.login'

config = Config("config.ini", "DEV")
logger = Logger(config.log,level=logging.DEBUG if config.DEBUG else logging.INFO,when='d').logger

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
from .main import bp_main

app.register_blueprint(auth)
app.register_blueprint(bp_main)
