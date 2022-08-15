# -*- coding: utf-8 -*-
from flask import jsonify, request, current_app, url_for, g
from flask.views import MethodView

from epaas.apis.v1 import api_v1
from epaas.apis.v1.auth import auth_required, generate_token, decrypt
from epaas.apis.v1.errors import api_abort, ValidationError
from epaas.apis.v1.schemas import user_schema, role_schema
from epaas.extensions import db
from epaas.models import User
from flask import current_app
import logging
import demjson
import time


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
        from epaas.apis.v1.endpoint import endpoint_schema
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
        ssh_user = data.get('ssh_user')
        password = data.get('password')
        endpoint = data.get('endpoint')
        roles = data.get('roles')

        from epaas.models import Endpoint, Server
        endpoint_server = Endpoint.query.filter_by(name=endpoint).first()
        if endpoint_server is None:
            endpoint = Endpoint(
                name=endpoint,
                path=endpoint,
                roles=roles
            )
            db.session.add(endpoint)
            db.session.commit()
        server = Server(
            name=name,
            ip=ip,
            ssh_user=ssh_user,
            password=password,
            roles=roles,
            endpoints=[endpoint_server]
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


class AppAPI(MethodView):
    decorators = [auth_required]

    def get(self):
        from epaas.apis.v1.app import applist_schema
        title = request.args.get('title')
        sort = request.args.get('sort')
        page = request.args.get('page')
        limit = request.args.get('limit')
        author = request.args.get('author')
        applist, length = applist_schema(title, sort, page, limit, author)
        return jsonify({
            'data': {
                'total': length,
                'items': applist
            },
            'code': 20000
        })

    def post(self):
        raw_data = request.get_data()
        data = demjson.decode(raw_data)

        name = data.get('appname')
        description = data.get('description')
        display_time = time.localtime()
        docker_images = data.get('imagename')
        module_env = data.get('module_env')
        modulename = data.get('modulename')
        author = data.get('author')

        from epaas.models import App
        app = App(
            name=name,
            description=description,
            display_time=display_time,
            docker_images=docker_images,
            module_env=module_env,
            modulename=modulename,
            author=author
        )
        db.session.add(app)
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
api_v1.add_url_rule('/app/list', view_func=AppAPI.as_view('applist'), methods=['GET'])
api_v1.add_url_rule('/app/create', view_func=AppAPI.as_view('appcreate'), methods=['POST'])
