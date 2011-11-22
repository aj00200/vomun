import unittest
import libs.browser

class BrowserRequiredVariables(unittest.TestCase):
    '''Test to make sure the required error classes exit.'''
    def test_platform_name_exists(self):
        self.assertIsNotNone(libs.browser.platform_name)

    def test_open_exists(self):
        self.assertIsNotNone(libs.browser.open)
