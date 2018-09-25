import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    SECRET_KEY = os.environ.get('SSBADM_SECRET_KEY') or 'you-will-never-guess'
    DB_NAME = os.environ.get('SSBADM_DB_NAME') or 'ssbadm'
    DB_HOST = os.environ.get('SSBADM_DB_HOST') or '10.63.253.66'
    DB_PORT = os.environ.get('SSBADM_DB_PORT') or '3306'
    DB_USER = os.environ.get('SSBADM_DB_USER') or 'ssbadm'
    DB_PASS = os.environ.get('SSBADM_DB_PASS') or 'kake10kake'
    DEBUG = os.environ.get('SSBADM_DEBUG') or False
    TESTING = os.environ.get('SSBADM_TESTING') or False
    CSRF_ENABLED = os.environ.get('SSBADM_CSRF_ENABLED') or True
    PORT = os.environ.get('SSBADM_PORT') or "80"
    ENV = os.environ.get('SSB_ENV') or "Production"


class ProductionConfig(Config):
    DEBUG = False


class StagingConfig(Config):
    DEVELOPMENT = True
    DEBUG = True


class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True
    PORT = "5000"


class TestingConfig(Config):
    TESTING = True