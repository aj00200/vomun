'''Holds common encryption functions/classes which will probably be used by
other encryption algorithms.
'''

class Encryption(object):
    '''Base object to contain encryption and keep the current session or
    encryption data tied with the peer which is being connected to. Other
    encryption methods should subclass this object.
    '''

    def encrypt(self, data):
        '''Encrypt `data` with this encryption algorithm.'''
        return data

    def decrypt(self, data):
        '''Decrypt `data` with this encryption algorithm.'''
        return data

    def sign(self, data):
        '''If this algorithm supports signatures, sign `data`. Otherwise,
        return `data` untouched.
        '''
        return data

    def verify(self, data):
        '''Preform any verifications such as signature verifications to make
        sure that the message is authentic. If the algorithm does not support
        verification, return True.
        '''
        return True
