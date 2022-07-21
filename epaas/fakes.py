# -*- coding: utf-8 -*-

import random

from faker import Faker
from sqlalchemy.exc import IntegrityError

from epaas.extensions import db
from epaas.models import User
from epaas.models import Role, Endpoint, Server

#fake = Faker()


def fake_user():
    test = User(
        username='bingjunx',
        name='xiao bingjun',
        introduction='hello flask',
        roles="editor"
    )
    test.set_password('bingjunx')
    db.session.add(test)
    db.session.commit()


def fake_role():
    test = Role(
        name='test',
        description='test role'
    )
    db.session.add(test)
    db.session.commit()


def fake_endpoint():
    test1 = Endpoint(
        name='test1',
        path='test1',
        roles="admin,editor"
    )
    db.session.add(test1)
    db.session.commit()


def fake_server():
    server1 = Server(
        name='server1',
        ip='192.168.1.1',
        roles="admin,editor",
        endpoints=[Endpoint.query.filter_by(name='test1').first()]
    )
    db.session.add(server1)
    db.session.commit()
