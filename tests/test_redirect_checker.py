import unittest
from redirect_checker import check_redirect

class TestRedirectChecker(unittest.TestCase):
    def test_no_redirect(self):
        self.assertIsNone(check_redirect("http://example.com"))

    def test_redirect(self):
        self.assertIsNone(check_redirect("http://github.com"))

if __name__ == '__main__':
    unittest.main()
