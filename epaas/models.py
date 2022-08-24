# -*- coding: utf-8 -*-

from datetime import datetime

from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from epaas.extensions import db


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20))
    password_hash = db.Column(db.String(128))
    name = db.Column(db.String(30))
    introduction = db.Column(db.Text)
    roles = db.Column(db.String(128))
    avatar = db.Column(db.String(128))
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def validate_password(self, password):
        return check_password_hash(self.password_hash, password)


class Role(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30))
    description = db.Column(db.Text)


# relationship table
endpoint_server = db.Table('endpoint_server',
                             db.Column('server_id', db.Integer, db.ForeignKey('server.id')),
                             db.Column('endpoint_id', db.Integer, db.ForeignKey('endpoint.id')))


class Endpoint(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))
    path = db.Column(db.String(20))
    roles = db.Column(db.String(30))
    servers = db.relationship('Server', secondary=endpoint_server, back_populates='endpoints')


class Server(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(10))
    ip = db.Column(db.String(20), unique=True)
    ssh_user = db.Column(db.String(10))
    password = db.Column(db.String(128))
    roles = db.Column(db.String(30))
    endpoints = db.relationship('Endpoint', secondary=endpoint_server, back_populates='servers')


class App(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(10), unique=True)
    description = db.Column(db.Text)
    display_time = db.Column(db.Time)
    docker_images = db.Column(db.JSON)
    module_env = db.Column(db.JSON)
    modulename = db.Column(db.JSON)
    author = db.Column(db.String(20))

