'''Holds common encryption functions/classes which will probably be used by
other encryption algorithms.
'''
import Crypto.PublicKey.RSA
import hashlib
import libs.config

KEY_PATH = libs.globals.global_vars['config']['keydir'] + '%s.key'
keys = {}

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
    '''Load the key from the KEY_PATH folder. Keys are stored by their sha256
    hash to prevent modification.'''
    # TODO: only hash the public key
    try:
        key_file = open(KEY_PATH % sha256, 'r')
        key_data = key_file.read()
        key_file.close()
        if sha256 == hashlib.sha256(key_data).hexdigest():
            keys[sha256] = Crypto.PublicKey.RSA.importKey(key_data)
        else:
            print('The key appears to be corrupt or modified.')
    except IOError:
        print('Key file, %s, could not be loaded.' % sha256)
        
def save_key(sha256):
    '''Save a key we have the sha256 hash of to the KEY_PATH folder.'''
    # TODO: only hash the public key
    try:
        key_data = keys[sha256].exportKey()
        key_file = open(KEY_PATH % sha256, 'w')
        key_file.write(key_data)
        key_file.close()
    except IOError:
        print('Key file, %s, could not be written.' % sha256)
        
def import_key(keydata):
    '''Import the key given in keydata.'''
    # TODO: only hash the public key
    key = Crypto.PublicKey.RSA.importKey(keydata)
    sha256 = hashlib.sha256(key.exportKey())
    keys[sha256] = key
    
    save_key(sha256)
    return True
        
def export_key(keyid, secret = False):
    '''Export the key with the given key ID. If `secret` is set to True, the
    entire key is exported. Otherwise, only the public key is exported.'''
    return 'Waiting for encryption to work.'
