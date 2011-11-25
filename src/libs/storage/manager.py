'''Manage the current data store. Hold onto information. Eventually dump old
information that has not been requested in a long time.
TODO: decide on how to store the data long term (persistent storage).
'''
import json
import hashlib
import libs.errors
import libs.events

class Block(object):
    max_size = 2048 # 2048 for now because of the RSA Crypto limit
    def __init__(self, data):
        if len(data) > self.max_size:
            raise libs.errors.AnonError('Block too big.')
        self.data = data
        self.hash = hashlib.sha256(data).hexdigest()
        # TODO: Decide on using sha256 or sha1 (or even sha512)^
        
class StorageDB(libs.events.Handler):
    '''An database type object to store and sort blocks.'''
    def __init__(self):
        self.usks = {}
        self.uuks = {}
        
    # Database methods
    def add_usk(self, block):
        self.usks[block.hash] = block
        
    def add_uuk(self, block):
        self.uuks[block.hash] = block
        
    def search(self, query):
        if query.type == 'UUK':
            if query.id in self.uuks:
                return self.uuks[query.id]
        elif query.type == 'USK':
            if query.id in self.usks:
                return self.usks[query.id]
            
    def load(self, path):
        '''Load the database from a storage file.'''
        pass
        
    def save(self, path):
        '''Save the database to a storage file.'''
        pass
        
    # Event methods
    def got_message(self, data):
        self.add_uuk(Block(data))
        
    def got_request(self, query):
        self.search(query)
        
class Query(object):
    def __init__(self, blocktype, id):
        self.type = blocktype
        self.id = id
        

def start():
    '''Create the storage database.'''
    database = StorageDB()
    libs.events.register_handler(database)
