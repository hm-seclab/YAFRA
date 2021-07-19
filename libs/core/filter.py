'''
This script contains function to eleminate duplicates from datastructures.
'''

from libs.kafka.logging import LogMessage

def filter_dict_values(dictionary, servicename):
    '''
    filter_dict_values will filter the all values of the type
        list from a given dict.
    @param dictionary will be the input dict.
    @return a filtered dict incase of an error the given dict
        will be returned.
    '''
    try:
        for key, values in dictionary.items():
            if isinstance(values, list) and len(values) > 0:
                dictionary[key] = list(set(values))
    except Exception as error:
        LogMessage(str(error), LogMessage.LogTyp.ERROR, servicename).log()
    return dictionary


def replace_item(finding, findings_key, blocked, servicename):
    '''
    replace_item will traverse over the finding and replace an
    blacklisted element from the finding object.
    @param name of the key where to filter.
    @param blocked will be the value which should be blocked.
    '''
    try:
        for f_key, f_values in finding.items():
            if isinstance(f_values, dict):
                finding[f_key] = replace_item(f_values, findings_key, blocked, servicename)
            if findings_key in finding:
                finding[findings_key] = list(filter(lambda x: x != blocked, finding[findings_key]))
    except Exception as error:
        LogMessage(str(error), LogMessage.LogTyp.ERROR, servicename).log()
    return finding

def filter_by_blacklist(findings, blacklist, servicename):
    '''
    filter_by_blacklist will filter the findings by the values in the blacklist.
    @param findings will be a dict with all findings.
    @param blacklist will be dict with all values to block.
    @servicename will be the name of the calling service.
    @return will return the filter findings as dict.
    '''

    try:
        if blacklist is not None:
            for name, blocks in blacklist.items():
                for block in blocks:
                    findings = replace_item(findings, name, block, servicename)
    except Exception as error:
        LogMessage(str(error), LogMessage.LogTyp.ERROR, servicename).log()
    return findings
