# -*- coding: utf-8 -*-
from flask import jsonify, request, current_app, url_for, g
from flask.views import MethodView

from auth.apis.v1 import api_v1
from auth.apis.v1.auth import auth_required, generate_token, decrypt
from auth.apis.v1.errors import api_abort, ValidationError
from auth.apis.v1.schemas import user_schema, role_schema
from auth.extensions import db
from auth.models import User
from flask import current_app
import logging
import demjson


def get_item_body():
    data = request.get_json()
    body = data.get('body')
    if body is None or str(body).strip() == '':
        raise ValidationError('The item body was empty or invalid.')
    return body


class IndexAPI(MethodView):

    def get(self):
        return jsonify({
            "api_version": "1.0",
            "api_base_url": "http://example.com/api/v1",
            "current_user_url": "http://example.com/api/v1/user",
            "authentication_url": "http://example.com/api/v1/token",
        })


class AuthTokenAPI(MethodView):

    def post(self):
        grant_type = request.form.get('grant_type')
        username = request.form.get('username')
        password_crypt = request.form.get('password')
        password = decrypt(password_crypt)
        #current_app.logger.debug(request.form)
        if grant_type is None or grant_type.lower() != 'password':
            return api_abort(code=400, message='The grant type must be password.')

        user = User.query.filter_by(username=username).first()
        if user is None or not user.validate_password(password):
            return api_abort(code=400, message='Either the username or password was invalid.')

        token, expiration = generate_token(user)

        response = jsonify({
            'data': {'token': token},
            'token_type': 'Bearer',
            'expires_in': expiration,
            'code': 20000
        })
        response.headers['Cache-Control'] = 'no-store'
        response.headers['Pragma'] = 'no-cache'
        return response


class UserAPI(MethodView):
    decorators = [auth_required]

    def get(self):
        return jsonify({
            'data': user_schema(g.current_user),
            'code': 20000
        })


class RoleAPI(MethodView):
    decorators = [auth_required]

    def get(self):
        return jsonify({
            'data': role_schema(),
            'code': 20000
        })


class EndpointAPI(MethodView):
    decorators = [auth_required]

    def get(self):
        from auth.apis.v1.endpoint import endpoint_schema
        current_app.logger.debug(endpoint_schema())
        return jsonify({
            'data': endpoint_schema(),
            'code': 20000
        })


class ServerAPI(MethodView):
    decorators = [auth_required]

    def post(self):
        # data = json.loads(data, strict=False)
        # print(data)
        raw_data = request.get_data()
        data = demjson.decode(raw_data)

        ip = data.get('serverip')
        name = data.get('servername')
        endpoint = data.get('endpoint')
        roles = data.get('roles')

        from auth.models import Endpoint, Server
        server = Server(
            name=name,
            ip=ip,
            roles=roles,
            endpoints=[Endpoint.query.filter_by(name=endpoint).first()]
        )
        db.session.add(server)
        db.session.commit()

        response = jsonify({
            'data': 'succeed',
            'code': 20000
        })
        response.headers['Cache-Control'] = 'no-store'
        response.headers['Pragma'] = 'no-cache'
        return response


api_v1.add_url_rule('/', view_func=IndexAPI.as_view('index'), methods=['GET'])
api_v1.add_url_rule('/oauth/token', view_func=AuthTokenAPI.as_view('token'), methods=['POST'])
api_v1.add_url_rule('/user', view_func=UserAPI.as_view('user'), methods=['GET'])
api_v1.add_url_rule('/role', view_func=RoleAPI.as_view('role'), methods=['GET'])
api_v1.add_url_rule('/server/endpoint', view_func=EndpointAPI.as_view('endpoint'), methods=['GET'])
api_v1.add_url_rule('/server/create', view_func=ServerAPI.as_view('create'), methods=['POST'])
