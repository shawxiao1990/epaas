# -*- coding: utf-8 -*-

from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
import logging

login_manager = LoginManager()
db = SQLAlchemy()


def log():
    # 创建一个logger
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    if not logger.handlers:
        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)
        formater = logging.Formatter('%(asctime)s %(module)s-%(lineno)d %(name)s %(levelname)s %(message)s')
        ch.setFormatter(formater)
        logger.addHandler(ch)
    return logger
