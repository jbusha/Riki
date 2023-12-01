# John Busha

import unittest
import os
from wiki.core import Page

class TestFileDownloadIntegration(unittest.TestCase):
    TEST_PAGES_DIR = os.path.join(os.getcwd(), 'Tests', 'TestPages')

    def setUp(self):
        self.page_path = os.path.join(self.TEST_PAGES_DIR, 'TestPage.md')
        self.page_url = "test_page"
        self.page = Page(self.page_path, self.page_url, new=True)

        self.page.title = 'Test Page'
        self.page.body = 'Test Body.'
        self.page.tags = 'test, page'

    def tearDown(self):
        if os.path.exists(self.TEST_PAGES_DIR):
            for root, dirs, files in os.walk(self.TEST_PAGES_DIR, topdown=False):
                for name in files:
                    os.remove(os.path.join(root, name))
                for name in dirs:
                    os.rmdir(os.path.join(root, name))
            os.rmdir(self.TEST_PAGES_DIR)

    def test_save_pdf_file_integration(self):
        self.page.save_pdf_file()

        pdf_path = self.page.get_file_path("pdf")

        self.assertTrue(os.path.isfile(pdf_path))
        self.assertEqual(os.path.splitext(pdf_path)[1].lower(), ".pdf")
        self.assertGreater(os.path.getsize(pdf_path), 0)

    def test_save_text_file_integration(self):
        self.page.save_text_file()

        txt_path = self.page.get_file_path("txt")

        self.assertTrue(os.path.isfile(txt_path))
        self.assertEqual(os.path.splitext(txt_path)[1].lower(), ".txt")
        self.assertGreater(os.path.getsize(txt_path), 0)

    def test_save_markdown_file_integration(self):
        self.page.save()

        md_path = self.page.get_file_path("md")

        self.assertTrue(os.path.isfile(md_path))
        self.assertEqual(os.path.splitext(md_path)[1].lower(), ".md")
        self.assertGreater(os.path.getsize(md_path), 0)

    def test_get_file_size_integration(self):
        self.page.save()

        md_size = self.page.get_file_size("md")
        txt_size = self.page.get_file_size("txt")
        pdf_size = self.page.get_file_size("pdf")

        self.assertGreater(md_size, 0)
        self.assertGreater(txt_size, 0)
        self.assertGreater(pdf_size, 0)

    def test_get_file_path_integration(self):
        test_pages_dir = TestFileDownloadIntegration.TEST_PAGES_DIR

        md_path = self.page.get_file_path("md")
        txt_path = self.page.get_file_path("txt")
        pdf_path = self.page.get_file_path("pdf")

        self.assertEqual(md_path, os.path.abspath(self.page.path))
        self.assertEqual(txt_path, os.path.join(test_pages_dir, 'txt', self.page.url + '.txt'))
        self.assertEqual(pdf_path, os.path.join(test_pages_dir, 'pdf', self.page.url + '.pdf'))

if __name__ == '__main__':
    unittest.main()