from io import BytesIO

from flask import send_file
from flask_restx import Namespace, Resource, fields

from models import PageText, PageImage
from helpers import packing

resources_api = Namespace('resources', description='Get downloaded resources (text content, images)')

_text = resources_api.model('Text', {
    'url': fields.String(required=True, description='The page URL'),
    'text': fields.String(required=True, description='The page text'),
})

_image = resources_api.model('Image', {
    'url': fields.String(required=True, description='The image URL'),
    'page_url': fields.String(required=True, description='The page URL'),
})


@resources_api.route('/texts')
class TextList(Resource):
    @resources_api.doc('text')
    @resources_api.marshal_list_with(_text)
    def get(self):
        """List all pages which have downloaded text"""

        return PageText.query.all()


@resources_api.route('/texts/<path:url>')
@resources_api.param('url', 'The page URL')
class Text(Resource):
    @resources_api.doc('get_text')
    @resources_api.marshal_with(_text)
    def get(self, url):
        """Get a text from given Url"""

        page_text = PageText.query.filter_by(url=url).first()

        return page_text or {'url': url, 'text': 'Resource not found'}


@resources_api.route('/images')
class ImageList(Resource):
    @resources_api.doc('image')
    @resources_api.marshal_list_with(_image)
    def get(self):
        """List all pages which have downloaded images"""

        return PageImage.query.all()


@resources_api.route('/images/<path:url>')
@resources_api.param('url', 'The page URL')
@resources_api.produces('application/octet-stream')
class Image(Resource):
    @resources_api.doc('get_image')
    def get(self, url):
        """Download images for given url"""

        images = [(img.url, img.image) for img in PageImage.query.filter_by(page_url=url).all()]

        if images:
            zip_file = packing.pack_files_into_archive(images)

            return send_file(BytesIO(zip_file), attachment_filename=f'img_{packing.fix_filename(url)}.zip',
                             as_attachment=True)

        else:
            return 'Resource not found'
