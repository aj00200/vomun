import unittest
import libs.encryption.base

class TestLibsEncryptionBase(unittest.TestCase):
    def test_Encryption_exists(self):
        '''Test if libs.encryption.base.Encryption exists. This class is
        required by the other encryption modules and should not change
        much without giving a lot of warning to the other develoers.'''
        self.assertIsNotNone(libs.encryption.base.Encryption)

    def test_Encryption_methods(self):
        '''Test if libs.encryption.base.Encryption has the necessary default
        messages which other encryption methods may not overwrite.'''
        self.assertIsNotNone(libs.encryption.base.Encryption.encrypt)
        self.assertIsNotNone(libs.encryption.base.Encryption.decrypt)
        self.assertIsNotNone(libs.encryption.base.Encryption.verify)
        self.assertIsNotNone(libs.encryption.base.Encryption.sign)

    
