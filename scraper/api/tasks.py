from flask import request
from flask_restplus import Namespace, Resource, fields

from extensions import db
from models import PageText, PageImage
from helpers import scraping

tasks_api = Namespace('tasks', description='Tasks related operations.')

_task = tasks_api.model('Task', {
    'id': fields.String(required=True, description='The task identifier'),
    'status': fields.String(required=True, description='The task status'),
})


@tasks_api.route('/')
class TaskList(Resource):
    @tasks_api.doc('list_tasks')
    @tasks_api.marshal_list_with(_task)
    def get(self):
        """List all tasks"""

        raise NotImplementedError()


@tasks_api.route('/<string:task_id>')
@tasks_api.param('task_id', 'The task identifier')
@tasks_api.response(404, 'Task not found')
class Task(Resource):
    @tasks_api.doc('get_task')
    @tasks_api.marshal_with(_task)
    def get(self, task_id):
        """Get a task given its identifier"""

        raise NotImplementedError()


@tasks_api.route('/collect_text')
@tasks_api.param('url', 'Url to page', _in='formData')
@tasks_api.response(404, 'Task not found')
class Task(Resource):
    @tasks_api.doc('task_collect_text')
    def post(self):
        """Collect text content from page"""

        # TODO: use task queue
        url = request.form['url']
        page_content = scraping.get_text_content(url)
        text = scraping.get_text_from_page(page_content)

        page_text = PageText(url=url, text=text)
        db.session.merge(page_text)
        db.session.commit()

        return url


@tasks_api.route('/collect_images')
@tasks_api.param('url', 'Url to page', _in='formData')
@tasks_api.response(404, 'Task not found')
class Task(Resource):
    @tasks_api.doc('task_collect_images')
    def post(self):
        """Collect images from page"""

        # TODO: use task queue
        page_url = request.form['url']
        page_content = scraping.get_text_content(page_url)
        images_relative_urls = scraping.get_images_relative_urls_from_page(page_content)
        images_urls = scraping.get_absolute_urls(page_url, images_relative_urls)

        for image_url in images_urls:
            image_data = scraping.get_bytes_content(image_url)

            page_image = PageImage(url=image_url, image=image_data, page_url=page_url)
            db.session.merge(page_image)
            db.session.commit()

        return page_url
