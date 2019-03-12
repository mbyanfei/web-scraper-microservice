import unittest

from helpers import scraping


class TestScraping(unittest.TestCase):
    def test_get_bytes_content_without_http_in_url(self):
        url = 'www.test.com'
        page_content = scraping.get_bytes_content(url)

        self.assertTrue(isinstance(page_content, bytes))

    def test_get_text_content_without_http_in_url(self):
        url = 'www.test.com'
        page_content = scraping.get_text_content(url)

        self.assertTrue(isinstance(page_content, str))

    def test_get_page_text_from_page(self):
        page_content = '<!DOCTYPE html><html><body><h1>Test heading</h1><p>Test paragraph</p></body></html>'
        expected_page_text = 'Test headingTest paragraph'

        self.assertEqual(expected_page_text, scraping.get_text_from_page(page_content))

    def test_get_page_text_from_page_with_style(self):
        page_content = '<!DOCTYPE html><html><body><h1>Test heading</h1><p style="background: red;">Test paragraph</p></body></html>'
        expected_page_text = 'Test headingTest paragraph'

        self.assertEqual(expected_page_text, scraping.get_text_from_page(page_content))

    def test_get_page_text_from_page_with_javascript(self):
        page_content = '<!DOCTYPE html><html><body><h1>Test heading</h1><script>alert(1);</script></body></html>'
        expected_page_text = 'Test heading'

        self.assertEqual(expected_page_text, scraping.get_text_from_page(page_content))

    def test_get_images_relative_urls_from_page(self):
        page_content = '<!DOCTYPE html><html><body><h1>Test heading</h1><img src="/img/test.png"></body></html>'
        expected_images_urls = ["/img/test.png"]

        self.assertEqual(expected_images_urls, scraping.get_images_relative_urls_from_page(page_content))

    def test_get_images_relative_urls_from_page_with_many_images(self):
        page_content = '<!DOCTYPE html><html><body><h1>Test heading</h1><img src="/img/test.png"><img src="/img/test2.png"></body></html>'
        expected_images_urls = ["/img/test.png", "/img/test2.png"]

        self.assertEqual(expected_images_urls, scraping.get_images_relative_urls_from_page(page_content))

    def test_get_absolute_url(self):
        relative_url = "/img/test.png"
        base_url = "http://www.test.com"
        expected_absolute_url = "http://www.test.com/img/test.png"

        self.assertEqual(expected_absolute_url, scraping.get_absolute_url(base_url, relative_url))

    def test_get_absolute_url_with_base_url_trailing_slash(self):
        relative_url = "/img/test.png"
        base_url = "http://www.test.com/"
        expected_absolute_url = "http://www.test.com/img/test.png"

        self.assertEqual(expected_absolute_url, scraping.get_absolute_url(base_url, relative_url))

    def test_get_absolute_url_with_relative_url_leading_double_slash(self):
        relative_url = "//text.com/img/test.png"
        base_url = "http://www.test.com"
        expected_absolute_url = "text.com/img/test.png"

        self.assertEqual(expected_absolute_url, scraping.get_absolute_url(base_url, relative_url))

    def test_get_absolute_urls(self):
        relative_urls = ["/img/test.png", "/img/test2.png"]
        base_url = "http://www.test.com"
        expected_absolute_urls = ["http://www.test.com/img/test.png", "http://www.test.com/img/test2.png"]

        self.assertEqual(expected_absolute_urls, scraping.get_absolute_urls(base_url, relative_urls))
