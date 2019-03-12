from flask import Flask

from api import api_blueprint
from extensions import db, migrate


def create_app(config='config.Config'):
    app = Flask(__name__)
    app.config.from_object(config)

    register_extensions(app)
    register_blueprints(app)

    return app


def register_extensions(app):
    db.init_app(app)
    migrate.init_app(app, db)


def register_blueprints(app):
    app.register_blueprint(api_blueprint, url_prefix='/api/v1')
