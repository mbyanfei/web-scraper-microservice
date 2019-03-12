import os

basedir = os.path.abspath(os.path.dirname(__file__))
env = os.environ


class Config:
    DEBUG = env.get('FLASK_ENV', 'dev') == 'dev'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    SECRET_KEY = env.get('SECRET_KEY') or 'change-me-on-production'
    SQLALCHEMY_DATABASE_URI = env.get('SQLALCHEMY_DATABASE_URI') or 'sqlite:///' + os.path.join(basedir, 'app.db')

    CELERY_RESULT_BACKEND = env.get('CELERY_RESULT_BACKEND')
    CELERY_BROKER_URL = env.get('CELERY_BROKER_URL')
    CELERY_TASK_SERIALIZER = 'json'
    CELERY_ACCEPT_CONTENT = ['json']
