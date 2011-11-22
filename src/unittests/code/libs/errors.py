import unittest
import libs.errors

class RequiredClasses(unittest.TestCase):
    '''Test to make sure the required error classes exit.'''
    def test_AnonError(self):
        self.assertIsNotNone(libs.errors.AnonError)
        self.assertTrue(issubclass(libs.errors.AnonError, Exception))

    def test_DependancyError(self):
        self.assertIsNotNone(libs.errors.DependancyError)
        self.assertTrue(issubclass(libs.errors.DependancyError,
                                   libs.errors.AnonError))

    def test_ConnectionError(self):
        self.assertIsNotNone(libs.errors.ConnectionError)
        self.assertTrue(issubclass(libs.errors.ConnectionError,
                                   libs.errors.AnonError))

    def test_ProtocolError(self):
        self.assertIsNotNone(libs.errors.ProtocolError)
        self.assertTrue(issubclass(libs.errors.ProtocolError,
                                   libs.errors.AnonError))

    def test_UsageError(self):
        self.assertIsNotNone(libs.errors.UsageError)
        self.assertTrue(issubclass(libs.errors.UsageError,
                                   libs.errors.AnonError))

    def test_InstallError(self):
        self.assertIsNotNone(libs.errors.InstallError)
        self.assertTrue(issubclass(libs.errors.InstallError,
                                   libs.errors.AnonError))
