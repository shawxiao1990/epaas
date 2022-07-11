# -*- coding: utf-8 -*-

from flask import url_for


def user_schema(user):
    return {
        'id': user.id,
        'self': url_for('.user', _external=True),
        'kind': 'User',
        'username': user.username,
        'roles': user.roles,
        'introduction': user.introduction
    }
