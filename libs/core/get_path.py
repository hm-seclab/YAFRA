'''
This script contains function to get the path for a given file.
'''
import os


def get_path(file, relpath):
    '''
    get_path will get the path
    for a given file.
    @param relpath will be the relative path to a file
    @return returns the path to the file.
    '''
    abspath = os.path.abspath(file)
    dirname = os.path.dirname(abspath)
    filepath = os.path.join(dirname, relpath)
    return filepath
