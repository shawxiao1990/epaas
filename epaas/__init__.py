# -*- coding: utf-8 -*-
import os
import click
import logging
from flask import Flask, render_template, request
from flask_login import current_user
from epaas.extensions import login_manager
from epaas.initdb import register_initdb_commands
from epaas.extensions import db
from flask_migrate import Migrate
from epaas.apis.v1 import api_v1
import logging
from flask.logging import default_handler
from epaas.config import config


def create_app(config_name=None):
    if config_name is None:
        config_name = os.getenv('FLASK_CONFIG', 'development')

    app = Flask('epaas')
    app.config.from_object(config[config_name])

    register_logger(app)
    register_extensions(app)
    register_initdb_commands(app)
    app.register_blueprint(api_v1, url_prefix='/api/v1')
    return app


def register_extensions(app):
    db.init_app(app)
    migrate = Migrate(app, db)
    #login_manager.init_app(app)


def register_logger(app):
    log_formatter = logging.Formatter("%(asctime)s [%(thread)d:%(threadName)s] %(filename)s:%(module)s:%(funcName)s in %(lineno)d] [%(levelname)s]: %(message)s")
    default_handler.setLevel(logging.DEBUG)
    default_handler.setFormatter(log_formatter)
    if not app.debug:
        app.logger.addHandler(default_handler)

