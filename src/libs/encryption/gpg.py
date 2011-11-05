'''Handles the encryption and decryption of messages we get and send.
Documentation on the gngpg module: https://code.google.com/p/python-gnupg/
'''
import libs.errors
import libs.globals
import libs.encryption.base
from api.functions import register_with_api

try:
    import gnupg
except ImportError:
    raise libs.errors.DependancyError(
        'Please install https://code.google.com/p/python-gnupg/')

try:
    gpg = gnupg.GPG(gnupghome = libs.globals.global_vars['config']['gnupgdir'])
except ValueError:
    raise libs.errors.DependancyError('GPG does not appear to be installed.')

class Encryption(libs.encryption.base.Encryption):
    '''Hold the GPG encryption state for a node.'''
    def __init__(self, source, dest):
        self.source = source # Key to sign with
        self.dest = dest     # Key to encrypt to
        
    def encrypt(self, string):
        '''Encrypt a message with public key, `keyid`'''
        # TODO: Eventually we want to switch armor to False (binary data)
        return gpg.encrypt(string, recipients = self.dest).data

    def sign(self, string):
        '''Sign string with `keyid`. This will not be used in P2P, but may be
        used for other messages.
        '''
        # TODO: make sure that this works
        return gpg.sign(string, keyid = self.source).data

    def decrypt(self, string):
        '''Decrypt `string`'''
        # TODO: make sure this actually works!
        return gpg.decrypt(string).data
        
    def verify(self, string):
        '''Verify the signature on `string` and return the signing key ID'''
        # TODO: make sure this actually works!
        return gpg.verify(string)

def generate_key(key_length = 2048, key_type = 'RSA', name = 'Anonymous'):
    '''Generate a key and return the key fingerprint'''
    # TODO: use the name parameter
    print('Generating a key. This could take a while.')
    key_data = gpg.gen_key_input(key_type = key_type, key_length = key_length)
    key = gpg.gen_key(key_data)

    return key.fingerprint

def export_key(fingerprint):
    '''Find a key with the given fingerprint and return the armored, public
    key. This needs to be done to add friends because friends need your public
    key to verify your identity and to encrypt information to you.
    '''
    print('Exporting %s' % fingerprint)
    return gpg.export_keys(fingerprint)

def import_key(data):
    '''Store a key. This will generally be used when adding friends.'''
    print('Importing key')
    return gpg.import_keys(data)
