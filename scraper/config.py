import os

basedir = os.path.abspath(os.path.dirname(__file__))
env = os.environ


class Config:
    DEBUG = env.get('FLASK_ENV', 'dev') == 'dev'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    SQLALCHEMY_DATABASE_URI = env.get('SQLALCHEMY_DATABASE_URI') or 'sqlite:///' + os.path.join(basedir, 'app.db')
