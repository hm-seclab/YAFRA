'''
Environment-varibale core libarys.
'''

import os

def envvar(name, default):
    '''
    envvar will get a environment-variable by its name. Incase
        the env-var is not set the default value will be returned.
    @param name will be the name of the env-var.
    @param default will be the default value.
    @return the env-var as a string.
    '''
    try:
        if (var := os.environ[name]) is not None:
            return var
        return default
    except KeyError:
        print("[i] Cannot access the environment-variable {} because it is not set.".format(name))
        return default
    except Exception as error:
        print("[-] An error occurred while trying to access the environment variable {}. Error: {}".format(name, error))
        return default
