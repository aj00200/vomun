'''Manage the current data store. Hold onto information. Eventually dump old
information that has not been requested in a long time.
TODO: decide on how to store the data long term (persistent storage).
'''
import hashlib
import libs.errors
import libs.events

class Block(object):
    max_size = 2048 # 2048 for now because of the RSA Crypto limit
    def __init__(self, data):
        if data > self.max_size:
            raise libs.errors.AnonError('Block too big.')
        self.data = data
        self.hash = hashlib.sha256(data).hexdigest()
        # TODO: Decide on using sha256 or sha1 (or even sha512)^
        
class StorageDB(libs.events.Handler):
    '''An database type object to store and sort blocks.'''
    def __init__(self):
        self.usks = {}
        self.uuks = {}
        
    def add_usk(self, block):
        self.usks[Block.hash] = Block
        
    def add_uuk(self, block):
        self.uuks[Block.hash] = Block
