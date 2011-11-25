'''Load the config from ~/.vomun/config.json'''

import os
import json
import libs.globals
from libs.morado.functions import register_with_api

CONFIG_PATH = os.path.expanduser("~/.vomun/config.json")


def open_config():
    '''Open the configuration file from ~/.vomun/config.json'''
    try:
        configfile = open(CONFIG_PATH,"r+")
    except IOError:
        default_config = {   
            'vomundir': os.getenv('HOME') + '/.vomun/',
            'gnupgdir': os.getenv('HOME') + '/.vomun/gnupg/',
            'nodekey': ''
        }
        configfile = open(CONFIG_PATH, 'a')
        configfile.write(json.dumps(default_config, indent = 4))
        configfile.flush()
        configfile.close()
        configfile = open(CONFIG_PATH, 'r+')
    return configfile


config_file = open_config()

@register_with_api
def load_config():
    '''Load the configuration file'''
    libs.globals.global_vars['config'] = json.loads(config_file.read())
    config_file.seek(0) # return read/write position to beginning of the file

@register_with_api
def get_config():
    '''Return the contents of the configuration file'''
    return libs.globals.global_vars["config"]


@register_with_api
def save_config():
    '''Write the configuration file to the hard disk'''
    config_file.write(json.dumps(libs.globals.global_vars['config'],
                                 indent = 4))

load_config()
