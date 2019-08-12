import os


class Config(object):
    DEBUG = False
    TESTING = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = 'postgresql://USER:PASSWORD@HOST/DATABASE'
    API_DIR = os.path.dirname(os.path.abspath(__file__))


class DefaultConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'postgresql://USER:PASSWORD@HOST/DATABASE'
    API_DIR = '/flask/'
