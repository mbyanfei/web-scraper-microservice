import unittest

from scraper.utils import scrap as scrap


class TestScraping(unittest.TestCase):
    def test_get_content_without_http_in_url(self):
        url = 'www.test.com'
        self.assertTrue(isinstance(scrap.get_page_content(url), bytes))

    def test_get_page_text_from_page(self):
        page_content = b'<!DOCTYPE html><html><body><h1>Test heading</h1><p>Test paragraph</p></body></html>'
        page_text = 'Test headingTest paragraph'

        self.assertEqual(scrap.get_text_from_page(page_content), page_text)

    def test_get_page_text_from_page_with_style(self):
        page_content = b'<!DOCTYPE html><html><body><h1>Test heading</h1><p style="background: red;">Test paragraph</p></body></html>'
        page_text = 'Test headingTest paragraph'

        self.assertEqual(scrap.get_text_from_page(page_content), page_text)

    def test_get_page_text_from_page_with_javascript(self):
        page_content = b'<!DOCTYPE html><html><body><h1>Test heading</h1><script>alert(1);</script></body></html>'
        page_text = 'Test heading'

        self.assertEqual(scrap.get_text_from_page(page_content), page_text)

    def test_get_images_relative_urls_from_page(self):
        page_content = b'<!DOCTYPE html><html><body><h1>Test heading</h1><img scraper="/img/test.png"></body></html>'
        images_urls = ["/img/test.png"]

        self.assertEqual(scrap.get_images_relative_urls_from_page(page_content), images_urls)

    def test_get_images_relative_urls_from_page_with_many_images(self):
        page_content = b'<!DOCTYPE html><html><body><h1>Test heading</h1><img scraper="/img/test.png"><img scraper="/img/test2.png"></body></html>'
        images_urls = ["/img/test.png", "/img/test2.png"]

        self.assertEqual(scrap.get_images_relative_urls_from_page(page_content), images_urls)

    def test_get_absolute_url(self):
        relative_url = "/img/test.png"
        base_url = "http://www.test.com"
        absolute_url = "http://www.test.com/img/test.png"

        self.assertEqual(scrap.get_absolute_url(base_url, relative_url), absolute_url)

    def test_get_absolute_url_with_base_url_trailing_slash(self):
        relative_url = "/img/test.png"
        base_url = "http://www.test.com/"
        absolute_url = "http://www.test.com/img/test.png"

        self.assertEqual(scrap.get_absolute_url(base_url, relative_url), absolute_url)

    def test_get_absolute_url_with_relative_url_leading_double_slash(self):
        relative_url = "//text.com/img/test.png"
        base_url = "http://www.test.com"
        absolute_url = "text.com/img/test.png"

        self.assertEqual(scrap.get_absolute_url(base_url, relative_url), absolute_url)

    def test_get_absolute_urls(self):
        relative_urls = ["/img/test.png", "/img/test2.png"]
        base_url = "http://www.test.com"
        absolute_urls = ["http://www.test.com/img/test.png", "http://www.test.com/img/test2.png"]

        self.assertEqual(scrap.get_absolute_urls(base_url, relative_urls), absolute_urls)
