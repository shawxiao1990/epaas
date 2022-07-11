# -*- coding: utf-8 -*-

import random

from faker import Faker
from sqlalchemy.exc import IntegrityError

from auth.extensions import db
from auth.models import User

fake = Faker()


def fake_admin():
    admin = User(
        username='admin',
        name='Mima Kirigoe',
        introduction='Um, l, Mima Kirigoe, had a fun time as a member of CHAM...',
        roles="admin"
    )
    admin.set_password('helloflask')
    db.session.add(admin)
    db.session.commit()
