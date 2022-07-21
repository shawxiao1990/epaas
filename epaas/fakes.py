# -*- coding: utf-8 -*-

import random

from faker import Faker
from sqlalchemy.exc import IntegrityError

from epaas.extensions import db
from epaas.models import User
from epaas.models import Role, Endpoint, Server

fake = Faker()


def fake_admin():
    admin = User(
        username='admin',
        name='Mima Kirigoe',
        introduction='Um, l, Mima Kirigoe, had a fun time as a member of CHAM...',
        roles="admin"
    )
    test = User(
        username='bingjunx',
        name='xiao bingjun',
        introduction='hello flask',
        roles="editor"
    )
    admin.set_password('helloflask')
    test.set_password('bingjunx')
    db.session.add(admin)
    db.session.add(test)
    db.session.commit()


def fake_role():
    admin = Role(
        name='admin',
        description='Super Administrator. Have access to view all pages.'
    )
    editor = Role(
        name='editor',
        description='Normal Editor. Can see all pages except permission page.'
    )
    visitor = Role(
        name='visitor',
        description='Just a visitor. Can only see the home page and the document page.'
    )
    db.session.add(admin)
    db.session.add(editor)
    db.session.add(visitor)
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
