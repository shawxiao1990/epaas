# -*- coding: utf-8 -*-

import random

from faker import Faker
from sqlalchemy.exc import IntegrityError

from auth.extensions import db
from auth.models import User
from auth.models import Role

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
