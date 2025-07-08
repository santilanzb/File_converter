import unittest
import os
from plugins.handler_factory import get_handler
from core.exceptions import UnsupportedFormatError, FileProcessingError

class TestFileHandlers(unittest.TestCase):
    """
    Tests conversion handlers for newly added plugins.
    """

    def setUp(self):
        """
        Setup for test cases.
        """
        self.temp_file = "temp_test_file"

    def tearDown(self):
        """
        Clean up after tests.
        """
        try:
            os.remove(self.temp_file)
        except Exception:
            pass

    def test_pdf_handler(self):
        handler = get_handler('pdf')
        self.assertIsNotNone(handler)

        with open(self.temp_file, 'wb') as f:
            f.write(b"%PDF-1.4\n1 0 obj\n<<\n/Type /Catalog\n/Outlines 2 0 R\n/Pages 3 0 R\n>>\nendobj\n")

        with self.assertRaises(FileProcessingError):
            handler.read(self.temp_file)

    def test_docx_handler(self):
        handler = get_handler('docx')
        self.assertIsNotNone(handler)

    def test_pptx_handler(self):
        handler = get_handler('pptx')
        self.assertIsNotNone(handler)

    def test_ppsx_handler(self):
        handler = get_handler('ppsx')
        self.assertIsNotNone(handler)

    def test_azw3_handler(self):
        with self.assertRaises(UnsupportedFormatError):
            get_handler('azw3')

    def test_mobi_handler(self):
        with self.assertRaises(UnsupportedFormatError):
            get_handler('mobi')


if __name__ == "__main__":
    unittest.main()
