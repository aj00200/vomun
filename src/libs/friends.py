'''This module loads a list of friends out of ~/.vomun/friends.json and parses
it into a list of Friend objects.
'''
import json
import os.path
import time
from tunnels import directudp
from libs.globals import global_vars
import libs.encryption.rsa
from libs.packets import parse_packets, packets_by_id, make_packet
from libs.morado.functions import register_with_api



global_vars['friends'] = {}
friendlistpath = os.path.expanduser('~/.vomun/friends.json')
friendlistr = open(friendlistpath, "r")


def load_friends():
    '''Load the List of friends'''
    friendsjson = json.loads(friendlistr.read())
    for friend in friendsjson:
        try:
            port = friend['port']
            keyid = friend['keyid']
            name = friend['name']
            ip = friend['lastip']
            friendo = Friend(keyid, ip, port, name)

            print friendo
            global_vars['friends'][keyid] = friendo

        except Exception as ex: 
            print(ex, friend)

@register_with_api
def save_friends():
    '''Write ~/.vomun/friends.json'''
    friendlistw = open(friendlistpath, 'w+')
    json_template = '''[
%s
]'''
    friendsjson = ','.join([friend._json() for friend in global_vars['friends'].values()])
    friendlistw.write(json_template % friendsjson)
    friendlistw.flush()

@register_with_api
def add_friend(keyid, ip, port = 1337, name = 'unknown'):
    '''Add a friend to our friends list'''
    friend_obj = Friend(keyid, ip, port, name)
    global_vars['friends'][keyid] = friend_obj
    save_friends()

@register_with_api
def del_friend(keyid):
    '''Delete a friend'''
    try:
        del global_vars['friends'][keyid]
    except:
        global_vars['logger'].info('Friend %s does not exist.' % keyid)


class Friend:
    '''Friend class, stores data related to a friend such as the Connection
    object and the encryption object. Handles data transfer and encryption.
    '''
    def __init__(self, keyid, ip, port=1337, name = 'unknown'):
        '''Defines a friend, can be used to send a message'''
        self.ip = ip
        self.port = port
        self.name = name
        self.keyid = keyid
        self.connected = False
        self.rconnection = None
        self.wconnection = None
        self.data = ''
        
        print('Setting up encryption. %s:%s' % (
                libs.globals.global_vars['config']['nodekey'], self.keyid))
        self.encryption = libs.encryption.rsa.Encryption(
                libs.globals.global_vars['config']['nodekey'], self.keyid)

    def parse_packets(self):
        print('parsing packets of %s' % self.name)
        self.__decrypt()
        packets, leftovers =  parse_packets(self.data)
        self.data = leftovers
        print('leftovers:', leftovers)
        for packet in packets:
            self.handle_packets(packet[0],packet[1])

    def handle_packets(self, packet_id, packet):
        '''Handle actions depending on the ID of the packet.'''
        if packet_id in packets_by_id: # Known packet type?
            packet_id = packets_by_id[packet_id]
        else: # The packet has an unknown ID
            reason = 'Invalid packetId: %i' % packet_id
            disc = make_packet('Disconnect',reasonType='Custom',
                               reason=reason,reasonlength=len(reason))
            self.send(disc)
            return
        
        # Take acctions depending on the type of packet
        if packet_id == 'ConnectionRequest':
            print('sending acceptConnection')
            #self.connected = True
            accept_connection = make_packet('AcceptConnection', int=1)
            self.send(accept_connection, 1)
            print('acceptConnection sent')

        elif packet_id == 'AcceptConnection':
            print('got acceptConnection')
            self.connected = True
            
        elif packet_id == 'Message':
            libs.events.broadcast('got_message', packet)
            
        else:
            print packet_id, packet

    def _begin_handshake(self):
        print 'shaking hands'
        ip = self.ip     # not sure what ip and key we need here?
        key=self.keyid   # ours or the friends?
        # encryptionmethod = "aes"
        packet = make_packet("ConnectionRequest", encryptionmethod="rsa",ip=ip,
                           iplength = len(ip), key = key, keylength = len(key))
        self.send(packet)

    def rename(self, newname):
        '''Rename the Friend'''
        self.name = newname

    def connect(self):
        '''Connect to the friend'''
        self.wconnection = directudp.Tunnel(self)
        self.wconnection.connect()
        #self.connected = True

    def send(self, data, system=0):
        '''Send data to the friend. Will try to establish a connection, if not yet connected'''
        if self.wconnection == None:
            self.connect()
            #if not self.connected:
            #    raise ConnectionError('Could not reach %s' % self.ip)
        #if not self.connected and not system:
        #    print 'not connected: Message discarded. Message was: %s' % message
        #    return
        message = self.encryption.encrypt(data)
        self.wconnection.send(message)

    def send_message(self, message):
        '''Sends a Text message to a friend'''
        keyid = self.keyid
        keyidlength = len(str(keyid))
        tstamp = time.time()
        messagelength = len(str(message))

        pack = make_packet("Message",to_node_length = keyidlength, to_node = keyid,
                            timestamp = tstamp, message_length = messagelength,
                            message = message)

        self.send(pack)
    def _json(self):
        '''Returns the json representation of a friend, used to save the friendlist'''
        return '''
    {
        "name": "%s",
        "keyid": "%s",
        "lastip": "%s",
        "port": %i    
    }''' % (self.name, self.keyid, self.ip, self.port)

    def _rpc(self):
        '''Returns the dict representation of the friend, used by the rpc server'''
        return {
            'name' : self.name,
            'keyid': self.keyid,
            'lastip' : self.ip,
            'port' : self.port
        }
        
    def __decrypt(self):
        self.data = self.encryption.decrypt(self.data)
        print('Decrypted data: %s' % self.data)
        
    def __str__(self):
        return '<friend %s on %s:%i with id %s>' % (
                self.name, self.ip, self.port, self.keyid)


## API section




@register_with_api
def get_friend_by_ip(ip):
    '''Search for a Friend object with the given ip and return it.'''
    for friend in global_vars['friends'].values():
        if friend.ip == ip:
            return friend

@register_with_api
def get_friend_by_name(name):
    '''Search for a Friend object with the given name and return it.'''
    for friend in global_vars['friends'].values():
        if friend.name == name:
            return friend

@register_with_api
def get_friend_by_key(keyid):
    '''Search for a Friend with the given key ID and return it.'''
    for friend in global_vars['friends'].values():
        if friend.keyid == keyid:
            return friend

@register_with_api
def friend_send(friendname, message):
    '''Send a message to a friend.'''
    return get_friend_by_name(friendname).send(message)


@register_with_api
def friend_connect(friendname):
    '''Connect to a friend with the given name.'''
    return get_friend_by_name(friendname).connect()


@register_with_api
def friend_rename(friendname, newname):
    '''Rename a friend.'''
    return get_friend_by_name(friendname).rename(newname)

@register_with_api
def friend_list():
    '''Return a list of friends.'''
    friendslist = [friend._rpc() for friend in global_vars['friends'].values()]
    return friendslist

@register_with_api
def friend_connect(friend):
    friend = get_friend_by_name(friend)
    friend.connect()
    friend._begin_handshake()