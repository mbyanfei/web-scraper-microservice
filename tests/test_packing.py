import unittest

from scraper.utils import pack as pack


class TestScraping(unittest.TestCase):
    def test_fix_filename_with_full_url(self):
        filename = "https://www.test.com/img/test.png"
        fixed = "https__www.test.com_img_test.png"

        self.assertEqual(pack.fix_filename(filename), fixed)
