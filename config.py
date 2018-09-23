import os

class Config:
    DEBUG = False
    TESTING = False
    SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class ProductionConfig(Config):
    pass
    #FLASK_ENV = 'production'
    #SECRET_KEY = 'supersecret' # set as an env var. To generate, python -c 'import os; print(os.urandom(16))'

class DevelopmentConfig(Config):
    #FLASK_ENV = 'development'
    DEBUG = True
    SECRET_KEY = 'dev'

class StagingConfig(Config):
    #FLASK_ENV = 'development'
    DEBUG = True

class TestingConfig(Config):
    TESTING = True
