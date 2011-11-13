#! /usr/bin/env python
print('''
=== Anon+ Setup ===
== Project Vomun ==
''')
import os
import hashlib
import libs.errors


try:
    import Crypto
    import Crypto.PublicKey.RSA
except ImportError:
    raise libs.errors.DependancyError('''PyCrypto is required to use Anon+
        Get it for Linux at https://www.dlitz.net/software/pycrypto/
        Get it for Windows at http://www.voidspace.org.uk/python/modules.shtml#pycrypto
    ''')
    
# Check PyCrpyto version basics - require v2.1.x or higher
if Crypto.version_info[0] < 2 or Crypto.version_info[1] < 1:
    raise libs.errors.DependancyError(
            'Please update PyCrypto: https://www.dlitz.net/software/pycrypto/')

## Prepare for setup
# Find local variables
print('[*] Preparing for setup...')
HOME = os.path.expanduser('~')
VOMUN_PATH = os.path.join(HOME, '.vomun')
KEYS_PATH = os.path.join(VOMUN_PATH, 'keys.json')
CONFIG_PATH = os.path.join(VOMUN_PATH, 'config.json')

USER_NAME = raw_input('Pick a user name: ')

# Setup file structure for Anon+
try:
    print(' [*] Making ~/.vomun/')
    os.mkdir(VOMUN_PATH, 0711)
except OSError as error:
    if error.errno == 17:
        print('  [*] %s already exists. Do not need to create.' % VOMUN_PATH)
    else:
        print('  [*] Error creating %s' % VOMUN_PATH)
        raise libs.errors.InstallError(
                     'Please check your file permissions for %s' % HOME)

## Key setup
# Generate 2048 bit node key
keys = {}
print('[*] Setting up encryption keys')
print(' [*] Generating a 2048 bit node key')
print('     this could take a while...')

# ####################################
# TODO: do non-symbolic key generation
# ####################################
keys['nodekey'] = Crypto.PublicKey.RSA.generate(2048)
keys['nodekey'].hash = hashlib.sha256(
        keys['nodekey'].publickey().exportKey()).hexdigest()

print('  [*] Done. Key fingerprint:')
print('      %s' % keys['nodekey'].hash)


# Generate 2048 bit identity key
print(' [*] Generating a 2048 bit identity key')
print('     this could take a while...')

# ####################################
# TODO: do non-symbolic key generation
# ####################################
keys['userkey'] = Crypto.PublicKey.RSA.generate(2048)
keys['userkey'].hash = hashlib.sha256(
        keys['userkey'].publickey().exportKey()).hexdigest()

print('  [*] Done. Key fingerprint:')
print('      %s' % keys['userkey'].hash)


## Configuration
# Generate the contents
print('[*] Generating the config file...')
# template = '''
# {
#     "keydir": "{keysdir}",
#     "vomundir": "{vomundir}",
#     "nodekey": "{nodekey}",
#     "userkey": "{userkey}",
#     "username": "{username}"
# }
# '''
template = '''{
    "keydir": "%s",
    "vomundir": "%s",
    "nodekey": "%s",
    "userkey": "%s",
    "username": "%s"
}'''

config = template % (KEYS_PATH.replace('\\', '\\\\'),
                     VOMUN_PATH.replace('\\', '\\\\'),
                     keys['nodekey'].hash,
                     keys['userkey'].hash,
                     USER_NAME
                    )

try:
    print(' [*] Writing the config file.')
    config_file = open(CONFIG_PATH, 'w')
    config_file.write(config)
    config_file.close()
except IOError as error:
    print('  [*] Error writing %s. Check file permissions' % CONFIG_PATH)
    raise libs.errors.InstallError('Could not write to %s.' % CONFIG_PATH)

friendlistpath = os.path.expanduser('~/.vomun/friends.json')
try:
        friendlistr = open(friendlistpath, "r")
        friendlistr.close()
except IOError:
        friendlistr = open(friendlistpath, "w")
        friendlistr.write('[]')
        friendlistr.close()
        
## Setup complete
print(' == Setup Complete ==')
print('''
 == Anon+ Setup is Complete ==
Please run vomun.py and then go to
http://localhost:7777/ to use it.
''')
os.system("vomun.py")
os.system("python vomun.py")

