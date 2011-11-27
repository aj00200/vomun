#! /usr/bin/env python
import gettext

translation = gettext.translation('setup', 'locale')
_ = t.ugettext

print(_('''
=== Anon+ Setup ===
== Project Vomun ==
'''))
import os
import json
import hashlib
import libs.errors

if __name__ != '__main__':
    exit() # Otherwise pydoc will run the setup


try:
    import Crypto
    import Crypto.PublicKey.RSA
except ImportError:
    raise libs.errors.DependancyError(_('''PyCrypto is required to use Anon+
        Get it for Linux at https://www.dlitz.net/software/pycrypto/
        Get it for Windows at http://www.voidspace.org.uk/python/modules.shtml#pycrypto
    '''))

# Check PyCrpyto version basics - require v2.1.x or higher
# The version in PyCrypto is incorrect. See bug #892944
if Crypto.version_info[0] < 2 or Crypto.version_info[1] < 1:
    raise libs.errors.DependancyError(_(
            'Please update PyCrypto: https://www.dlitz.net/software/pycrypto/'))

## Prepare for setup
# Find local variables
print(_('[*] Preparing for setup...'))
HOME = os.path.expanduser('~')
VOMUN_PATH = os.path.join(HOME, '.vomun', '')
KEYS_PATH = os.path.join(VOMUN_PATH, 'keys.json')
CONFIG_PATH = os.path.join(VOMUN_PATH, 'config.json')

USER_NAME = raw_input('Pick a user name: ')

# Setup file structure for Anon+
try:
    print(_(' [*] Making ~/.vomun/'))
    os.mkdir(VOMUN_PATH, 0711)
except OSError as error:
    if error.errno == 17:
        print(_('  [*] %s already exists. Do not need to create.' % VOMUN_PATH))
    else:
        print(_('  [*] Error creating %s' % VOMUN_PATH))
        raise libs.errors.InstallError(_(
                     'Please check your file permissions for %s' % HOME))

## Key setup
# Generate 2048 bit node key
keys = {}
print(_('[*] Setting up encryption keys'))
print(_(' [*] Generating a 2048 bit node key'))
print(_('     this could take a while...'))

# ####################################
# Generate the node-key for the user
# ####################################
try:
    keys['nodekey'] = Crypto.PublicKey.RSA.generate(2048)
    keys['nodekey'].hash = hashlib.sha256(
            keys['nodekey'].publickey().exportKey()).hexdigest()
except AttributeError:
    pass # Waiting for input from the PyCrypto people

print(_('  [*] Done. Key fingerprint:'))
print(_('      %s' % keys['nodekey'].hash))


# Generate 2048 bit identity key
print(_(' [*] Generating a 2048 bit identity key'))
print(_('     this could take a while...'))

# ####################################
# Generate the user-key for the user
# ####################################
keys['userkey'] = Crypto.PublicKey.RSA.generate(2048)
keys['userkey'].hash = hashlib.sha256(
        keys['userkey'].publickey().exportKey()).hexdigest()

print(_('  [*] Done. Key fingerprint:'))
print(_('      %s' % keys['userkey'].hash))

# Write keys
print(_('[*] Writing keys to keys.json'))
keys_by_hash = {
    keys['nodekey'].hash: keys['nodekey'].exportKey(),
    keys['userkey'].hash: keys['userkey'].exportKey()
}
try:
    key_file = open(KEYS_PATH, 'w')
    key_file.write(json.dumps(keys_by_hash, indent = 4))
    key_file.close()
except IOError:
    print(_('  [*] Error writing %s. Check file permissions.' % KEY_PATH))
    raise libs.errors.InstallError(_('Could not write to %s.' % KEY_PATH))


## Configuration
# Generate the contents
print(_('[*] Generating the config file...'))
config = json.dumps({
    'keyfile': KEYS_PATH.replace('\\', '\\\\'),
    'vomundir': VOMUN_PATH.replace('\\', '\\\\'),
    'nodekey': keys['nodekey'].hash,
    'userkey': keys['userkey'].hash,
    'username': USER_NAME
}, indent = 4)

try:
    print(_(' [*] Writing the config file.'))
    config_file = open(CONFIG_PATH, 'w')
    config_file.write(config)
    config_file.close()
except IOError as error:
    print(_('  [*] Error writing %s. Check file permissions.' % CONFIG_PATH))
    raise libs.errors.InstallError(_('Could not write to %s.' % CONFIG_PATH))

friendlistpath = os.path.expanduser('~/.vomun/friends.json')
try:
        friendlistr = open(friendlistpath, "r")
        friendlistr.close()
except IOError:
        friendlistr = open(friendlistpath, "w")
        friendlistr.write('[]')
        friendlistr.close()

## Setup complete
print(_(' == Setup Complete =='))
print(_('''
 == Anon+ Setup is Complete ==
Please run vomun.py and then go to
http://localhost:7777/ to use it.
'''))
os.system("vomun.py")
os.system("python vomun.py")

