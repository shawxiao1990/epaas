# -*- coding: utf-8 -*-

from flask import url_for
from auth.apis.v1.auth import get_roles

def user_schema(user):
    return {
        'id': user.id,
        'self': url_for('.user', _external=True),
        'kind': 'User',
        'username': user.username,
        'roles': user.roles,
        'introduction': user.introduction
    }


def role_schema():
    roles_array = []
    roles = get_roles()
    for role in roles:
        role_json = {
            'id': role.id,
            'name': role.name,
            'description': role.description
        }
        roles_array.append(role_json)
    return roles_array
