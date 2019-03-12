from flask import Blueprint
from flask_restplus import Api

from .tasks import tasks_api
from .resources import resources_api

api_blueprint = Blueprint('api', __name__, url_prefix='/api/v1')
api = Api(api_blueprint, doc='/docs')

api.add_namespace(resources_api)
api.add_namespace(tasks_api)
