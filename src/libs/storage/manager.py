'''Manage the current data store. Hold onto information. Eventually dump old
information that has not been requested in a long time.
TODO: decide on how to store the data long term (persistent storage).
'''
import json
import hashlib

import libs
import libs.errors
import libs.events

class Block(object):
    '''A class which is used to store data. It is currently limited to 2048
    bits because of the current RSA crypto restrictions.
    '''
    max_size = 2048 # 2048 for now because of the RSA Crypto limit
    def __init__(self, data):
        if len(data) > self.max_size:
            raise libs.errors.AnonError('Block too big.')
        self.data = data
        self.hash = hashlib.sha256(data).hexdigest()
        # TODO: Decide on using sha256 or sha1 (or even sha512)^
        # TODO: Store a last-access timestamp

class StorageDB(libs.events.Handler):
    '''An database type object to store and sort blocks.'''
    def __init__(self):
        self.usks = {}
        self.uuks = {}

    # Database methods
    def add_usk(self, block):
        '''Add a USK block to the data store.'''
        self.usks[block.hash] = block

    def add_uuk(self, block):
        '''Add a UUK block to the data store.'''
        self.uuks[block.hash] = block

    def search(self, query):
        '''Search the database for a block which matches the query.'''
        if query.type == 'UUK':
            if query.id in self.uuks:
                return self.uuks[query.id]
        elif query.type == 'USK':
            if query.id in self.usks:
                return self.usks[query.id]

    def save(self, path):
        '''Save the database from a storage file.'''
        out_json = {}
        for block in self.uuks.values():
            out_json[block.hash] = block.data

        db_file = open(path, 'w') # TODO: possibly make a backup?
        db_file.write(json.dumps(out_json, indent = 2))
        db_file.close()

        libs.events.broadcast('logthis', 'Saved the data store.')

    def load(self, path):
        '''Load the database to a storage file.'''
        db_file = open(path, 'r')
        db_json = json.loads(db_file.read())
        db_file.close

        for block in db_json:
            self.uuks[block] = db_json[block]

    # Event methods
    def got_message(self, packet):
        '''Got a message. For now we are assuming that the message needs to be
        stored but this is not necessarily the case. In future versions we will
        have a custom packet for messages which need to be stored by other
        nodes. By default we are using UUK and there is a 100% chance that we
        will store this packet. There is no file size limit.
        '''
        message = packet.message
        self.add_uuk(Block(message))

    def got_request(self, query):
        '''Got a request for a data block.'''
        self.search(query)

    def shutdown(self):
        '''Save the data store into a file.'''
        self.save(self.path)

class Query(object):
    def __init__(self, blocktype, id):
        self.type = blocktype
        self.id = id


def start():
    '''Create the storage database.'''
    database = StorageDB()
    database.path = libs.config['vomundir'] + 'blocks.json'
    libs.events.register_handler(database)
