# -*- coding: utf-8 -*-
from flask import Blueprint
# from flask_cors import CORS

api_v1 = Blueprint('api_v1', __name__)

# CORS(api_v1)


from epaas.apis.v1 import resources
from epaas.apis.v1 import ssh
