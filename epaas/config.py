# -*- coding: utf-8 -*-

import os

BASEDIR = os.path.abspath(os.path.dirname(__file__))


class Config:
    """base config"""


class DevelopmentConfig(Config):
    """运行环境配置"""
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:password@127.0.0.1:3306/epaas'
    CRYPTO_KEY = '1234567890123456'
    CRYPTO_IV = '1234567890123456'


config = {
    'development': DevelopmentConfig
}
