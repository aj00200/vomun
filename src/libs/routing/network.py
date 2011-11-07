'''Manage our local view of the network, route between nodes, and make
suggestions about which nodes should switch locations.'''
import random

class Node(object):
    def __init__(self):
        self.connections = []
        self.location = random.randint(0,99999) # TODO: get a better number

    def add_connection(self, connection):
        '''Add a connection to a Node object'''
        self.connections.append(connection)

    def del_connection(self, connection):
        '''Remove a connection to a Node object.'''
        self.connections.remove(connection)
    
