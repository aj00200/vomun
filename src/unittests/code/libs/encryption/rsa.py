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

    def test_key_export(self):
        '''Make sure that key exports work. If not, PyCrypto may need to
        be updated to the latest version. python-crypto on Ubuntu 11.10
        is not sufficient for this purpose.'''
        key = RSA.generate(1024)
        key.exportKey()
        key.publickey().exportKey()

class TestLibsEncryptionRSA(unittest.TestCase):
    def test_global_variables_exist(self):
        '''Check that the needed global variables exist.'''
        self.assertIsNotNone(libs.encryption.rsa.keys)
        self.assertIsNotNone(libs.encryption.rsa.KEY_PATH)
        
    def test_functions_exist(self):
        self.assertIsNotNone(libs.encryption.rsa.generate_key)
        self.assertIsNotNone(libs.encryption.rsa.load_keys)
        self.assertIsNotNone(libs.encryption.rsa.save_keys)
        self.assertIsNotNone(libs.encryption.rsa.import_key)
        self.assertIsNotNone(libs.encryption.rsa.export_key)
        
    def test_key_generation(self):
        key = libs.encryption.rsa.generate_key(1024)
        self.assertTrue(isinstance(key, RSA._RSAobj))
        
    def test_class_methods_exist(self):
        self.assertIsNotNone(libs.encryption.rsa.Encryption)
        self.assertIsNotNone(libs.encryption.rsa.Encryption.encrypt)
        self.assertIsNotNone(libs.encryption.rsa.Encryption.decrypt)
