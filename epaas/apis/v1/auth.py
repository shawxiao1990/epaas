# -*- coding: utf-8 -*-
from functools import wraps

from flask import g, current_app, request
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer, BadSignature, SignatureExpired

from epaas.apis.v1.errors import api_abort, invalid_token, token_missing
from epaas.models import User, Role
from epaas.apis.v1 import api_v1
from flask_login import logout_user, login_required
from Crypto.Cipher import AES
import base64


# 填充函数
def add_to_16(value):
    while len(value.encode('utf-8')) % 16 != 0:
        value += '\x00'   #  补全, 明文和key都必须是16的倍数
    return value.encode('utf-8')


# 解密
def decrypt(en_str):
    iv = current_app.config['CRYPTO_IV']
    key = current_app.config['CRYPTO_KEY']
    # 解密时必须重新构建aes对象
    aes = AES.new(key=add_to_16(key), mode=AES.MODE_CBC, IV=iv.encode())
    # 先把密文转换成字节型, 再解密, 最后把之前填充的'\x00' 去掉
    decryptedstr = aes.decrypt(base64.decodebytes(en_str.encode(encoding='utf-8'))).decode().strip('\x00')
    # decryptedstr = aes.decrypt(a2b_hex(en_str)).decode().strip('\x00') # 对应上面的hex编码
    return decryptedstr


def get_roles():
    roles = Role.query.all()
    return roles


def generate_token(user):
    expiration = 3600
    s = Serializer(current_app.config['SECRET_KEY'], expires_in=expiration)
    token = s.dumps({'id': user.id}).decode('ascii')
    return token, expiration


def validate_token(token):
    s = Serializer(current_app.config['SECRET_KEY'])
    try:
        data = s.loads(token)
    except (BadSignature, SignatureExpired):
        return False
    user = User.query.get(data['id'])
    if user is None:
        return False
    g.current_user = user
    return True


def get_token():
    # Flask/Werkzeug do not recognize any authentication types
    # other than Basic or Digest, so here we parse the header by hand.
    if 'X-Token' in request.headers:
        try:
            #token_type, token = request.headers['Authorization'].split(None, 1)
            token = request.headers['X-Token']
            token_type = 'bearer'
        except ValueError:
            # The Authorization header is either empty or has no token
            token_type = token = None
    elif 'token' in request.args:
        try:
            token = request.args['token']
            token_type = 'bearer'
        except ValueError:
            # The Authorization header is either empty or has no token
            token_type = token = None
    else:
        token_type = token = None

    return token_type, token


def auth_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token_type, token = get_token()

        # Flask normally handles OPTIONS requests on its own, but in the
        # case it is configured to forward those to the application, we
        # need to ignore authentication headers and let the request through
        # to avoid unwanted interactions with CORS.
        if request.method != 'OPTIONS':
            if token_type is None or token_type.lower() != 'bearer':
                return api_abort(400, 'The token type must be bearer.')
            if token is None:
                return token_missing()
            if not validate_token(token):
                return invalid_token()
        return f(*args, **kwargs)

    return decorated
