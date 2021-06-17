'''
This script contains functions to handle and interact with misp for searching through stuff.
'''

from libs.kafka.logging import LogMessage

def get_appearance_in_misp(misp_handle, target, servicename):
    '''
    get_appearance_in_misp will return the appearance of a ioc in misp.
    @param misp_handle will be a handle to the misp platform.
    @param target will be the value to search for.
    @param servicename will be the name of the calling service.
    @return a string will all findings.
    '''
    appearance = ""
    try:
        appearance = misp_handle.search('events', 'json', value=target)
        if appearance is not None:
            appearance = [element['Event']['id'] for element in appearance]
            appearance = ", ".join(appearance)
    except Exception as error:
        LogMessage(str(error), LogMessage.LogTyp.ERROR, servicename).log()
    return appearance
