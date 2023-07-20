import os
basedir = os.path.abspath(os.path.dirname(__file__))


#https://www.digitalocean.com/community/tutorials/how-to-structure-a-large-flask-application-with-flask-blueprints-and-flask-sqlalchemy

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard to guess pass'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevelopmentConfig(Config):
    SQLALCHEMY_DATEBASE_URI = 'sqlite:///' + os.path.join(basedir, 'dev.sqlite')

class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATEBASE_URI = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')

class ProductionConfig(Config):
    SQLALCHEMY_DATEBASE_URI = 'sqlite:///' + os.path.join(basedir, 'production.sqlite')

config = {
    'development':DevelopmentConfig,
    'testing':TestConfig,
    'production':ProductionConfig
}