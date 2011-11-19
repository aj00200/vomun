'''Holds common encryption functions/classes which will probably be used by
other encryption algorithms.
'''
import Crypto.PublicKey.RSA
import hashlib
import json
import libs.config

KEY_PATH = libs.globals.global_vars['config']['keyfile']
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
        return keys[self.dest].encrypt(data, '')

    def decrypt(self, data):
        '''Decrypt `data` with this encryption algorithm.'''
        return keys[self.source].decrypt(data)

    def sign(self, data):
        '''Create a RSA signature for the given data'''
        return data

    def verify(self, data):
        '''Preform a verification on the RSA signature.'''
        return True

def generate_key(key_length = 2048):
    '''Generate an RSA key of the given key length.'''
    new_key = Crypto.PublicKey.RSA.generate(key_length)
    sha256 = hashlib.sha256(new_key.publickey().exportKey()).hexdigest()
    keys[sha256] = new_key
    save_keys()
    return new_key

def load_keys():
    '''Load the key from the KEY_PATH folder. Keys are stored by their sha256
    hash to prevent modification.'''
    # TODO: only hash the public key
    try:
        key_file = open(KEY_PATH, 'r')
        key_data = key_file.read()
        key_file.close()

        key_data = json.loads(key_data)
        for key in key_data:
            keys[key] = Crypto.PublicKey.RSA.importKey(key_data[key])
            
    except IOError:
        print('Key file, %s, could not be loaded.' % sha256)
        
def save_keys():
    '''Save all keys to ~/.vomun/keys.json'''
    # Make a backup first, keys.json.bak
    try:
        old_file = open(KEY_PATH, 'r')
        old_contents = old_file.read()
        old_file.close()
        
        backup_file = open(KEY_PATH + '.bak', 'w')
        backup_file.write(old_contents)
        backup_file.close()
    except IOError:
        print('Could not make backup of key file.')
        
    # Write the new data, keys.json
    key_data = {}
    for key in keys:
        key_data[key] = keys[key].exportKey()
        
    try:
        new_file = open(KEY_PATH, 'w')
        new_file.write(json.dumps(key_data, indent = 4))
        new_file.close()
    except IOError:
        print('Could not write updated key file.')
        
def import_key(keydata):
    '''Import the key given in keydata.'''
    key = Crypto.PublicKey.RSA.importKey(keydata)
    sha256 = hashlib.sha256(key.publickey().exportKey()).hexdigest()
    keys[sha256] = key
    
    save_keys()
    return sha256
        
def export_key(hash, secret = False):
    '''Export the key with the given key ID. If `secret` is set to True, the
    entire key is exported. Otherwise, only the public key is exported.'''
    if secret:
        return keys[hash].exportKey()
    else:
        return keys[hash].publickey().exportKey()

## Get ready
load_keys()