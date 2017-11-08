class Config(object):
    DEBUG = False
    TESTING = False

    # Secret key for dev; change if actually deploying
    SECRET_KEY = '''not_so_secret_key'''

    # Use Unicode utf8 in json
    JSON_AS_ASCII = False

    # SQLAlchemy stuff
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class DevConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///app_dev.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = True
