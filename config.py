import os

class Config():
    DEBUG = False
    TESTING = False
    SECRET_KEY = b'L\xb0\xf1rug\xb3\x9a\xd2Se\xad\x15\xc5zd\xba\xbd\x81'
    SQLALCHEMY_DATABASE_URI = "mysql://root:@localhost/domain_keeper"
    ENCRYPTION_KEY = os.environ.get("ENCRYPTION_KEY")

class ProductionConfig(Config):
    pass


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = "mysql://root:@localhost/domain_keeper"


class TestingConfig(Config):
    DEBUG = True
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "mysql://root:@localhost/domain_keeper"
