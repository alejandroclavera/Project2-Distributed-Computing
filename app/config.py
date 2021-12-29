import os

BASE_URL = '/mytube/api/'

class Config(object):
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']


class ProductionConfig(Config):
    DEBUG = False


class StagingConfig(Config):
    DEVELOPMENT = True
    DEBUG = True


class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True
    JSON_SORT_KEYS = False


class TestingConfig(Config):
    TESTING = True
    DEBUG = True
    JSON_SORT_KEYS = False
    SQLALCHEMY_DATABASE_URI = os.environ['TEST_DATABASE_URL']

app_config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
}
