'''
This script contains function to support merging common python datastructurs.
'''

from libs.kafka.logging import LogMessage

def merge_dicts(target, source, servicename):
    '''
    merge_dicts will take to dicts and merge them into one.
    @param target will be the first dict and also the final
        one.
    @param source will be the second dict, which gets put
        in to the first.
    @servicename will be the name of the calling service.
    @return a dict which will be the merge of the first and
        second. Incase of an error the target will be
        returned.
    '''
    try:
        duplicated_keys = list(filter(lambda src_k: src_k in target.keys(), source.keys()))
        target = {**source, **target}
        for key in duplicated_keys: 
            if isinstance(target[key], list):
                val = target[key]
                target[key] = val + source[key]
            else:
                continue
    except Exception as error:
        LogMessage(str(error), LogMessage.LogTyp.ERROR, servicename).log()
    return target
