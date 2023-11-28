import unittest

import os

from wiki.core import Page


class TestPage(unittest.TestCase):
    def setUp(self):
        path = os.path.join(os.getcwd(), 'Tests', 'TestPages', 'TestPage.md')
        url = "test_page"
        self.page = Page(path, url, new=True)

        self.page.title = 'Test Page'
        self.page.body = 'This is a test page.'
        self.page.tags = 'test, page'
        self.page.save()

    def test_save(self):        
        self.assertTrue(os.path.isfile(self.page.get_file_path("txt")))
        self.assertTrue(os.path.isfile(self.page.get_file_path("md")))
        self.assertTrue(os.path.isfile(self.page.get_file_path("pdf")))

    def test_get_file_size(self):
        self.assertTrue(self.page.get_file_size("txt") > 0)
        self.assertTrue(self.page.get_file_size("md") > 0)
        self.assertTrue(self.page.get_file_size("pdf") > 0)

if __name__ == '__main__':
    unittest.main()