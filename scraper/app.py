from celery import Celery
from flask import Flask


def create_app(config='config.Config', with_blueprints=True):
    app = Flask(__name__)
    app.config.from_object(config)

    register_extensions(app)
    if with_blueprints:
        register_blueprints(app)

    return app


def create_celery_app(app=None):
    app = app or create_app(with_blueprints=False)
    celery = Celery(app.name, backend=app.config['CELERY_RESULT_BACKEND'], broker=app.config['CELERY_BROKER_URL'])
    celery.conf.update(app.config)
    TaskBase = celery.Task

    class ContextTask(celery.Task):
        abstract = True

        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)

    celery.Task = ContextTask

    return celery


def register_extensions(app):
    from extensions import db, migrate

    db.init_app(app)
    migrate.init_app(app, db)


def register_blueprints(app):
    from api import api_blueprint

    app.register_blueprint(api_blueprint, url_prefix='/api/v1')
