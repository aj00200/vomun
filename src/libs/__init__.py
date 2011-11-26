import json
import os

CONFIG_PATH = os.path.expanduser('~/.vomun/config.json')

## Setup global variables
globals = {
    'running': True,
    'anon+': {
        'VERSION': 'v0.2.0',
        'BUILD': 5,
    }
}

globals['anon+']['banner'] = '''
======================
= Anon+ %s
= Build: %s
======================
'''

## Load and setup the configuration file
class Configuration(dict):
    '''A class to hold the contents of configuration files.'''
    path = CONFIG_PATH
    def load(self):
        '''Load the configuration file from the location set in self.path.
        The loaded data is parsed for json contents.
        '''
        try:
            config_file = open(self.path, 'r')
            values = json.loads(config_file.read())
            config_file.close()

            for value in values:
                self[value] = values[value]

        except IOError:
            self['vomundir'] = os.path.expanduser('~/.vomun/')
            self['nodekey'] = ''
            self.save()

    def save(self):
        '''Save the configuration enteries in a json format to the location set
        in self.path.
        '''
        config_file = open(self.path, 'w')
        config_file.write(json.dumps(self, indent = 2))
        config_file.close()

# Load the config file
config = Configuration()
config.load()