
import libs
import libs.threadmanager

libs.globals['apifunctions'] = {}

def register_with_api(func):
    libs.globals['apifunctions'][func.__name__] = func
    return func

@register_with_api
def get_functions():
    '''lists the api functions'''
    return [func.__name__ for func in libs.globals['apifunctions'].values()]

@register_with_api
def help(funcname):
    func = None
    for f in  libs.globals.global_vars['apiserver'].calls:
        if f.__name__ == funcname:
            func = f
            break
    return func.__doc__

@register_with_api
def shutdown():
    '''shuts down the server'''
    libs.globals.global_vars['running'] = False
    libs.threadmanager.killall()
    libs.threadmanager.close_sockets()
    return True

@register_with_api
def get_build():
    '''Return the build number'''
    return libs.globals['anon+']['BUILD']

# Functions for the config file
@register_with_api
def reload_config():
    '''Reload the configuration file.'''
    libs.config.load()

@register_with_api
def get_config():
    '''Return the contents of the configuration file.'''
    return libs.config

@register_with_api
def save_config():
    '''Save the contents of the configuration file.'''
    libs.config.save()
