'''
This script contains function to sanitize the title for gitlab branches.
'''
import hashlib
import re

from libs.kafka.logging import LogMessage


def sanitize_title(unsanitized_title, servicename):
    '''
    sanitize_title will take an unsanitized title as input
    and removes any special chars, which could possible violate
    the gitlab branch naming rules.
    @param unsanitized_title will be the unsanitized title in string format.
        @param servicename will be the name of the service calling this function.
    @return a sanitized title without any special chars except - in string format.
    '''
    sanitized_title = hashlib.md5(unsanitized_title.encode('UTF-8')).hexdigest() # nosec
    try:
        unsanitized_title = unsanitized_title.replace(' ', '-')
        sanitized_title = re.sub('[^A-Za-z0-9-]+', '', unsanitized_title)
    except Exception as error:
        LogMessage(str(error), LogMessage.LogTyp.ERROR, servicename).log()
    return sanitized_title