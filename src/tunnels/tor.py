'''Tunnel to use to connect to other nodes over tor.'''

class Tunnel(object):
    '''Base Tunnel class. Should be subclassed by other tunnels for
    compatibility reasons as well as ease of use.
    '''
    def __init__(self, node):
        pass # TODO: need to get node onion address and port
    
    def connect(self, address, port):
        '''Use this tunnel to connect to `address`:`port`'''
        pass

    def disconnect(self, nodeid):
        '''Disconnect from a node at `nodeid`'''
        pass

class Connection(object):
    '''A class to store a connection to a peer'''
    pass # TODO: need to get a SOCKS proxy socket running
