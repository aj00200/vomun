'''Provide the basic tools necessary to open an Internet browser.'''
import platform
import os

platform_name = platform.system()

def open(url):
    '''Open a browser to the given URL'''
    if platform_name == 'Windows':
        os.system('start %s' % url)
    if platform_name == 'Darwin':
        os.system('safari %s' % url)
    else:
        os.system('firefox %s' % url)