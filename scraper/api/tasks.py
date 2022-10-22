from celery.result import AsyncResult
from flask import request
from flask_restx import Namespace, Resource, fields

from worker import celery_app

tasks_api = Namespace('tasks', description='Tasks related operations.')

_task_status = tasks_api.model('TaskStatus', {
    'id': fields.String(required=True, description='The task identifier'),
    'status': fields.String(required=True, description='The task status'),
})


@tasks_api.route('/status/<string:task_id>')
@tasks_api.param('task_id', 'The task identifier')
@tasks_api.response(404, 'Task not found')
class TaskStatus(Resource):
    @tasks_api.doc('get_task')
    @tasks_api.marshal_with(_task_status)
    def get(self, task_id):
        """Get a task status given its identifier"""

        result = AsyncResult(task_id)

        return {'id': task_id, 'status': result.state}


@tasks_api.route('/collect_text')
@tasks_api.param('url', 'Url to page', _in='formData')
@tasks_api.response(404, 'Task not found')
class Task(Resource):
    @tasks_api.doc('task_collect_text')
    @tasks_api.marshal_with(_task_status)
    def post(self):
        """Collect text content from page"""

        url = request.form['url']
        task = celery_app.send_task('collect_text', args=[url])

        return {'id': task.id}


@tasks_api.route('/collect_images')
@tasks_api.param('url', 'Url to page', _in='formData')
@tasks_api.response(404, 'Task not found')
class Task(Resource):
    @tasks_api.doc('task_collect_images')
    @tasks_api.marshal_with(_task_status)
    def post(self):
        """Collect images from page"""

        url = request.form['url']
        task = celery_app.send_task('collect_images', args=[url])

        return {'id': task.id}
