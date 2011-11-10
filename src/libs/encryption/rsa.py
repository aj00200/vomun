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
        
    def encrypt(data):
        '''Encrypt `data` with this encryption algorithm.'''
        return data

    def decrypt(data):
        '''Decrypt `data` with this encryption algorithm.'''
        return data

    def sign(data):
        '''If this algorithm supports signatures, sign `data`. Otherwise,
        return `data` untouched.
        '''
        return data

    def verify(data):
        '''Preform any verifications such as signature verifications to make
        sure that the message is authentic. If the algorithm does not support
        verification, return True.
        '''
        return True

def generate_key(key_length = 2408):
    '''Generate an RSA key of the given key length.'''
    new_key = Crypto.PublicKey.RSA.generate(key_length)

def load_key(sha256):
    key_path = libs.globals.global_vars['config']['keypath'] + '%s.key'
    try:
        key_file = open(key_path % sha256, 'r')
    except IOError:
        print('Key file, %s, could not be loaded. % sha256')
