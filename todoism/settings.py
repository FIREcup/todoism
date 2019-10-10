import os

basedir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))


class BaseConfig:
    TODOISM_ITEM_PER_PAGE = 20

    SECRET_KEY = os.getenv('SECRET_KEY', 'a secret string')

    SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevelopmentConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://python:123@localhost:3306/todoism'
    REDIS_URL = 'redis://localhost'


class ProductionConfig(BaseConfig):
    pass


class TestingConfig(BaseConfig):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///'
    WTF_CSRF_ENABLED = False


config = {
        'development': DevelopmentConfig,
        'production': ProductionConfig,
        'testing': TestingConfig
}

