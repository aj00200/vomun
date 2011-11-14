import unittest
import Crypto

import Crypto.PublicKey.RSA as RSA
import libs.encryption.rsa

class TestPyCryptoRSA(unittest.TestCase):
    def test_version_number(self):
        '''Test to make sure we are using a somewhat sane version number.'''
        self.assertTrue(Crypto.version_info[0] > 1)
        self.assertTrue(Crypto.version_info[1] > 0)

    def test_key_generation(self):
        '''Generate a small, 1024bit RSA key to make sure generation works.'''
        RSA.generate(1024)

    def test_encryption(self):
        '''Make sure the key can encrypt and decrypt properly.'''
        key = RSA.generate(1024)
        enc = key.encrypt('Hello world', 'this is random data')
        dec = key.decrypt(enc)
        self.assertEqual(dec, 'Hello world')

class TestLibsEncryptionRSA(unittest.TestCase):
    def test_functions_exist(self):
        self.assertIsNotNone(libs.encryption.rsa.generate_key)
        self.assertIsNotNone(libs.encryption.rsa.load_keys)
        self.assertIsNotNone(libs.encryption.rsa.save_keys)
        self.assertIsNotNone(libs.encryption.rsa.import_key)
        self.assertIsNotNone(libs.encryption.rsa.export_key)
        
    def test_key_generation(self):
        key = libs.encryption.rsa.generate_key(1024)
        self.assertTrue(isinstance(key, RSA._RSAobj))
