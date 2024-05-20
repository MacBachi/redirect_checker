import unittest
import sys
import os

# Add the parent directory to sys.path so that the redirect_checker module can be imported
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from redirect_checker import check_redirect

class TestRedirectChecker(unittest.TestCase):
    def test_no_redirect(self):
        # This is a placeholder test; you'll need a URL that doesn't redirect
        self.assertIsNone(check_redirect("http://example.com"))

    def test_redirect(self):
        # This is a placeholder test; you'll need a URL that redirects
        self.assertIsNone(check_redirect("http://github.com"))

if __name__ == '__main__':
    unittest.main()

