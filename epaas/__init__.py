# -*- coding: utf-8 -*-
import os
import click
import logging
from flask import Flask, render_template, request
from flask_login import current_user
from epaas.extensions import login_manager
from epaas.settings import config
from epaas.initdb import register_initdb_commands
from epaas.extensions import db
#from epaas.extensions import migrate
from epaas.apis.v1 import api_v1
import logging
from flask.logging import default_handler


def create_app(config_name=None):
    if config_name is None:
        config_name = os.getenv('FLASK_CONFIG', 'development')

    app = Flask('epaas')
    app.config.from_object(config[config_name])
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:password@127.0.0.1:3306/epaas'
    app.config['CRYPTO_KEY'] = '1234567890123456'
    app.config['CRYPTO_IV'] = '1234567890123456'

    register_logger(app)
    register_extensions(app)
    register_initdb_commands(app)
    app.register_blueprint(api_v1, url_prefix='/api/v1')
    return app


def register_extensions(app):
    db.init_app(app)
    #login_manager.init_app(app)


def register_logger(app):
    log_formatter = logging.Formatter("%(asctime)s [%(thread)d:%(threadName)s] %(filename)s:%(module)s:%(funcName)s in %(lineno)d] [%(levelname)s]: %(message)s")
    default_handler.setLevel(logging.DEBUG)
    default_handler.setFormatter(log_formatter)
    if not app.debug:
        app.logger.addHandler(default_handler)

