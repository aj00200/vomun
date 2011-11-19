
import libs.globals
import libs.threadmanager

libs.globals.global_vars["apifunctions"] = {}

def register_with_api(func):
    libs.globals.global_vars["apifunctions"][func.__name__] = func
    return func

@register_with_api
def get_functions():
    '''lists the api functions'''
    return [func.__name__ for func in libs.globals.global_vars['apifunctions'].values()]

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
    return libs.globals.global_vars['anon+']['BUILD']
