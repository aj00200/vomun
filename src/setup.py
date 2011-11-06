#! /usr/bin/env python
print('''
=== Anon+ Setup ===
== Project Vomun ==
''')
import os
import libs.errors


try:
    import gnupg
except ImportError:
    import platform
    os1 = platform.system()
    raise libs.errors.DependancyError(
                'Please install https://code.google.com/p/python-gnupg/')
    if os1 == 'Windows':
        os.system("start http://www.gpg4win.org/")
    if os1 == 'Darwin':
        os.system('safari http://macgpg.sourceforge.net/')
    else:
        os.system("firefox http://www.gnupg.org/")

## Prepare for setup
# Find local variables
print('[*] Preparing for setup...')
HOME = os.path.expanduser('~')
VOMUN_PATH = os.path.join(HOME, '.vomun')
KEYS_PATH = os.path.join(VOMUN_PATH, 'keys')
CONFIG_PATH = os.path.join(VOMUN_PATH, 'config.json')

USER_NAME = raw_input('Pick a user name: ')

# Setup file structure for Anon+
try:
    print(' [*] Making ~/.vomun/')
    os.mkdir(VOMUN_PATH, 0711)
except OSError as error:
    if error.errno != 17:
        print('  [*] Error creating %s' % VOMUN_PATH)
        raise libs.errors.InstallError(
                     'Please check your file permissions for %s' % HOME)
    else:
        print('  [*] %s already exists. Do not need to create.' % VOMUN_PATH)

try:
    print(' [*] Making ~/.vomun/gpg/')
    os.mkdir(KEYS_PATH, 0700)
except OSError as error:
    if error.errno != 17:
        print('  [*] Error creating %s' % KEYS_PATH)
        raise libs.errors.InstallError(
                '      Please check your file permissions on %s' % VOMUN_PATH)
    else:
        print('  [*] %s already exists. Do not need to create.' % KEYS_PATH)
        
# Setup python-gpg to use ~/.vomun/keys
try:
    gpg = gnupg.GPG(gnupghome = KEYS_PATH)
except ValueError:
    raise libs.errors.DependancyError('Please install GPG: http://gnupg.org/')

## Key setup
# Generate 2048 bit node key
print('[*] Setting up encryption keys')
print(' [*] Generating a 2048 bit node key')
print('     this could take a while...')

key_data = gpg.gen_key_input(key_type = 'RSA', key_length = 2048,
                             name_real = 'Anonymous Node Key',
                             name_email = 'anonymous')
key = gpg.gen_key(key_data)
fingerprint = key.fingerprint

print('  [*] Done. Key fingerprint:')
print('      ' + fingerprint)

# Generate 2048 bit identity key
print(' [*] Generating a 2048 bit identity key')
print('     this could take a while...')

idkey_data = gpg.gen_key_input(key_type = 'RSA', key_length = 2048,                               
                               name_real = USER_NAME, # TODO: Allow password
                               name_email = 'anonymous')
idkey = gpg.gen_key(idkey_data)
idfingerprint = idkey.fingerprint

print('  [*] Done. Key fingerprint:')
print('      ' + idfingerprint)

## Configuration
# Generate the contents
print('[*] Generating the config file...')
# template = '''
# {
#     "gnupgdir": "{keysdir}",
#     "vomundir": "{vomundir}",
#     "nodekey": "{nodekey}",
#     "userkey": "{userkey}",
#     "username": "{username}"
# }
# '''
template = '''{
    "gnupgdir": "%s",
    "vomundir": "%s",
    "nodekey": "%s",
    "userkey": "%s",
    "username": "%s"
}'''

config = template % (KEYS_PATH.replace('\\', '\\\\'),
                     VOMUN_PATH.replace('\\', '\\\\'),
                     fingerprint,
                     idfingerprint,
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

