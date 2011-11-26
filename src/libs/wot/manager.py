'''Manages the network of WOT identities.'''
import libs.threadmanager

class Network(object):
    def __init__(self):
        self.network = {}

    def add_identity(self, identity):
        '''Add an identity to the network for tracking.'''
        self.network[identity.key] = identity

class UpdateThread(libs.threadmanager.Thread):
    '''A thread to manage the updating of enteries in the WOT. Information
    needs to be pulled out of the USK for each identity.'''
    pass
