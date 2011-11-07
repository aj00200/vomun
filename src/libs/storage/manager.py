'''Manage the current data store. Hold onto information. Eventually dump old
information that has not been requested in a long time.
TODO: decide on how to store the data long term (persistent storage).
'''
import hashlib

class Block(object):
    def __init__(self, data):
        self.data = data
        self.hash = hashlib.sha256(data).hexdigest()
        # TODO: Decide on using sha256 or sha1 (or even sha512)^
