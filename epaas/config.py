# -*- coding: utf-8 -*-

import os
import sys

BASEDIR = os.path.abspath(os.path.dirname(__file__))

# SQLite URI compatible
WIN = sys.platform.startswith('win')
if WIN:
    prefix = 'sqlite:///'
else:
    prefix = 'sqlite:////'

class Config:
    """base config"""
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev key')


class DevelopmentConfig(Config):
    """运行环境配置"""
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', prefix + os.path.join(BASEDIR, 'data-dev.db'))
    CRYPTO_KEY = '1234567890123456'
    CRYPTO_IV = '1234567890123456'


class TestingConfig(Config):
    TESTING = True
    WTF_CSRF_ENABLED = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'  # in-memory database


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', prefix + os.path.join(BASEDIR, 'data.db'))
    CRYPTO_KEY = os.getenv('CRYPTO_KEY', '1234567890123456')
    CRYPTO_IV = os.getenv('CRYPTO_IV', '1234567890123456')


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig
}
