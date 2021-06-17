'''
This script contains functions to handle ISO-Country-Codes.
'''

import pycountry

from libs.kafka.logging import LogMessage

def convert_alpha_2_to_alpha_3(alpha_2_c, servicename):
    '''
    
    '''
    try:
        country = pycountry.countries.get(alpha_2=alpha_2_c)
        return "Unknown" if country is None else country.alpha_3
    except Exception as error:
        LogMessage(str(error), LogMessage.LogTyp.ERROR, SERVICENAME).log()
        return "Unknown"

def convert_alpha_2_to_qualified_name(alpha_2_c, servicename):
    '''
    
    '''
    try:
        country = pycountry.countries.get(alpha_2=alpha_2_c)
        return "Unknown" if country is None else country.name
    except Exception as error:
        LogMessage(str(error), LogMessage.LogTyp.ERROR, SERVICENAME).log()
        return "Unknown"
