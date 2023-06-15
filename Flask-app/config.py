class Config(object):
    DEBUG = False
    TESTING = False

    # Made up keys etc. for tutorial. Do not push in a real app etc.
    SECRET_KEY = "iuhto743yto34iuho287gh78"

    DB_NAME = "production-db"
    DB_USERNAME = "root"
    DB_PASSWORD = "example"

    UPLOADS = "/home/username/Flask-app/app/static/images/uploads"

    SESSION_COOKIE_SECURE = True


class ProductionConfig(Config):
    pass


class DevelopmentConfig(Config):
    DEBUG = True
    DB_NAME = "development-db"
    DB_USERNAME = "root"
    DB_PASSWORD = "example"

    UPLOADS = "/home/michael/learning/py/Flask-app/app/static/images/uploads"

    SESSION_COOKIE_SECURE = False


class TestingConfig(Config):
    TESTING = True

    DB_NAME = "development-db"
    DB_USERNAME = "root"
    DB_PASSWORD = "example"

    UPLOADS = "/home/michael/learning/py/Flask-app/app/static/images/uploads"

    SESSION_COOKIE_SECURE = False
