'''Generate 256bit hashes of files. Used to verify that the files are trusted
by people who you trust. For example, a devloper can publish trust for a
version of vomun.py. This file can be easily used to check that.'''
import hashlib

def hash(path):
    '''Generate a Sha256 hash of a file and return it.'''
    file_obj = open(expand(path), 'r')
    hash = hashlib.sha256()
    buffer = file_obj.read(4096)
    while buffer:
        hash.update(buffer)
        buffer = file_obj.read(4096)
    return hash.hexdigest()
        
def expand(path):
    '''Expand variables within a path such as {vomun} and {src}. This should be
    replaced with the complete path to those files.'''
    return path # TODO: actually do something here
