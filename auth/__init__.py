# -*- coding: utf-8 -*-
import os
import click
import logging
from flask import Flask, render_template, request
from flask_login import current_user
from auth.extensions import login_manager
from auth.settings import config
from auth.models import User
from auth.extensions import db
from auth.apis.v1 import api_v1
import logging
from flask.logging import default_handler


def create_app(config_name=None):
    if config_name is None:
        config_name = os.getenv('FLASK_CONFIG', 'development')

    app = Flask('auth')
    app.config.from_object(config[config_name])

    register_logger(app)
    register_extensions(app)
    register_commands(app)
    app.register_blueprint(api_v1, url_prefix='/api/v1')
    return app


def register_extensions(app):
    db.init_app(app)
    login_manager.init_app(app)


def register_logger(app):
    log_formatter = logging.Formatter("%(asctime)s [%(thread)d:%(threadName)s] %(filename)s:%(module)s:%(funcName)s in %(lineno)d] [%(levelname)s]: %(message)s")
    default_handler.setLevel(logging.DEBUG)
    default_handler.setFormatter(log_formatter)
    if not app.debug:
        app.logger.addHandler(default_handler)


def register_commands(app):
    @app.cli.command()
    @click.option('--drop', is_flag=True, help='Create after drop.')
    def initdb(drop):
        """Initialize the database."""
        if drop:
            click.confirm('This operation will delete the database, do you want to continue?', abort=True)
            db.drop_all()
            click.echo('Drop tables.')
        db.create_all()
        click.echo('Initialized database.')

    @app.cli.command()
    @click.option('--username', prompt=True, help='The username used to login.')
    @click.option('--password', prompt=True, hide_input=True,
                  confirmation_prompt=True, help='The password used to login.')
    def init(username, password):
        """Building Bluelog, just for you."""

        click.echo('Initializing the database...')
        db.create_all()

        admin = User.query.first()
        if admin is not None:
            click.echo('The administrator already exists, updating...')
            admin.username = username
            admin.set_password(password)
        else:
            click.echo('Creating the temporary administrator account...')
            admin = User(
                username=username,
                name='Admin',
                introduction='Anything about you.'
            )
            admin.set_password(password)
            db.session.add(admin)

        db.session.commit()
        click.echo('Done.')

    @app.cli.command()
    def forge():
        """Generate fake data."""
        from auth.fakes import fake_admin

        db.drop_all()
        db.create_all()

        click.echo('Generating the administrator...')
        fake_admin()

        click.echo('Done.')
