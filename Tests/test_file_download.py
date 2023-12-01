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

    def tearDown(self):
        path = os.path.join(os.getcwd(), 'Tests', 'TestPages')
        for root, dirs, files in os.walk(path, topdown=False):
            for name in files:
                os.remove(os.path.join(root, name))
            for name in dirs:
                os.rmdir(os.path.join(root, name))
        os.rmdir(path)

    def test_save_txt_exists(self):        
        self.assertTrue(os.path.isfile(self.page.get_file_path("txt")))

    def test_save_md_exists(self):
        self.assertTrue(os.path.isfile(self.page.get_file_path("md")))

    def test_save_pdf_exists(self):
        self.assertTrue(os.path.isfile(self.page.get_file_path("pdf")))

    def test_get_file_size_txt(self):
        self.assertTrue(self.page.get_file_size("txt") > 0)

    def test_get_file_size_md(self):
        self.assertTrue(self.page.get_file_size("md") > 0)

    def test_get_file_size_pdf(self):
        self.assertTrue(self.page.get_file_size("pdf") > 0)

    def test_get_file_size_txt_greater(self):
        prev_size = self.page.get_file_size("txt")
        self.page.body = "This is a test page. It has been changed."
        self.page.save()
        self.assertTrue(self.page.get_file_size("txt") > prev_size)

    def test_get_file_size_md_greater(self):
        prev_size = self.page.get_file_size("md")
        self.page.body = "This is a test page. It has been changed."
        self.page.save()
        self.assertTrue(self.page.get_file_size("md") > prev_size)

    def test_get_file_size_pdf_greater(self):
        prev_size = self.page.get_file_size("pdf")
        self.page.body = "This is a test page. It has been changed."
        self.page.save()
        self.assertTrue(self.page.get_file_size("pdf") > prev_size)

    def test_get_missing_file_size_pdf(self): # Getting the size of a missing file should save the file if it doesn't exist
        path = self.page.get_file_path("pdf")
        os.remove(path)
        self.assertFalse(os.path.isfile(path))
        self.assertTrue(self.page.get_file_size("pdf") > 0)

    def test_get_missing_file_size_md(self):
        path = self.page.get_file_path("md")
        os.remove(path)
        self.assertFalse(os.path.isfile(path))
        self.assertTrue(self.page.get_file_size("md") > 0)

    def test_get_missing_file_size_txt(self):
        path = self.page.get_file_path("txt")
        os.remove(path)
        self.assertFalse(os.path.isfile(path))
        self.assertTrue(self.page.get_file_size("txt") > 0)

if __name__ == '__main__':
    unittest.main()