import unittest

from helpers import packing


class TestPacking(unittest.TestCase):
    def test_fix_filename_with_full_url(self):
        filename = "https://www.test.com/img/test.png"
        expected_fixed = "https__www.test.com_img_test.png"

        self.assertEqual(expected_fixed, packing.fix_filename(filename))
