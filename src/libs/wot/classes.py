'''Classes which are used to create the Web of Trust.'''

class Identity(object):
    '''A class to store trust information and connection information about an
    identity. This information can be used to calculate trust in the network.
    '''
    def __init__(self, key, trust = 0):
        self.key = key
        self.trust = 0
