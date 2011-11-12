'''Holds common encryption functions/classes which will probably be used by
other encryption algorithms.
'''
import Crypto.PublicKey.RSA
import libs.config

class Encryption(object):
    '''Base object to contain encryption and keep the current session or
    encryption data tied with the peer which is being connected to. Other
    encryption methods should subclass this object.
    '''
    def __init__(self, source, dest):
        self.source = source
        self.dest = dest
        
    def encrypt(self, data):
        '''Encrypt `data` with this encryption algorithm.'''
        return data

    def decrypt(self, data):
        '''Decrypt `data` with this encryption algorithm.'''
        return data

    def sign(self, data):
        '''Create a RSA signature for the given data'''
        return data

    def verify(self, data):
        '''Preform a verification on the RSA signature.'''
        return True

def generate_key(key_length = 2048):
    '''Generate an RSA key of the given key length.'''
    new_key = Crypto.PublicKey.RSA.generate(key_length)

def load_key(sha256):
    key_path = libs.globals.global_vars['config']['keypath'] + '%s.key'
    try:
        key_file = open(key_path % sha256, 'r')
    except IOError:
        print('Key file, %s, could not be loaded. % sha256')
        
def import_key(keydata):
    '''Import the key given in keydata.'''
    return 'Key importing not ready.'
        
def export_key(keyid):
    '''Export the key with the given key ID'''
    return 'Waiting for encryption to work.'
