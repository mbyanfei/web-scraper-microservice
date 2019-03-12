import unittest

from app import create_app
from extensions import db as _db
from models import PageText, PageImage


class TestApp(unittest.TestCase):
    def setUp(self):
        self.app = create_app('tests.TestConfig')
        self.db = _db

        self.client = self.app.test_client()
        self.ctx = self.app.app_context()

        self.ctx.push()
        self.db.create_all()

    def tearDown(self):
        self.db.drop_all()
        self.ctx.pop()

    def test_init_app(self):
        response = self.client.get('/api/v1/docs')
        expected_response_status_code = 200

        self.assertEqual(expected_response_status_code, response.status_code)

    def test_init_db(self):
        tables = self.db.metadata.tables.keys()
        expected_tables = ['page_text', 'page_image']

        self.assertEqual(expected_tables, list(tables))

    def test_insert_into_db(self):
        new_page_text = PageText(url='www.test.com', text='Example text')
        self.db.session.add(new_page_text)
        self.db.session.commit()

        page_texts = PageText.query.all()
        self.assertEqual(1, len(page_texts))

        page_text = page_texts[0]

        self.assertEqual('Example text', page_text.text)

    def test_get_text_list(self):
        new_page_text = PageText(url='www.test.com', text='Example text')
        self.db.session.add(new_page_text)
        new_page_text2 = PageText(url='www.test2.com', text='Example text2')
        self.db.session.add(new_page_text2)
        self.db.session.commit()

        response = self.client.get('/api/v1/resources/texts')
        texts = response.json
        expected_texts_count = 2

        self.assertEqual(expected_texts_count, len(texts))

    def test_get_text(self):
        new_page_text = PageText(url='www.test.com', text='Example text')
        self.db.session.add(new_page_text)
        self.db.session.commit()

        response = self.client.get('/api/v1/resources/texts/www.test.com')
        text = response.json['text']
        expected_text = 'Example text'

        self.assertEqual(expected_text, text)

    def test_get_image_list(self):
        new_page_image = PageImage(url='www.test.com/img/test.png', image=b'', page_url='www.test.com')
        self.db.session.add(new_page_image)
        new_page_image2 = PageImage(url='www.test2.com/img/test2.png', image=b'', page_url='www.test2.com')
        self.db.session.add(new_page_image2)
        self.db.session.commit()

        response = self.client.get('/api/v1/resources/images')
        texts = response.json
        expected_texts_count = 2

        self.assertEqual(expected_texts_count, len(texts))

    def test_get_page_images(self):
        new_page_image = PageImage(url='www.test.com/img/test.png', image=b'', page_url='www.test.com')
        self.db.session.add(new_page_image)
        self.db.session.commit()

        response = self.client.get('/api/v1/resources/images/www.test.com')
        expected_content_type = 'application/zip'

        self.assertEqual(expected_content_type, response.content_type)
