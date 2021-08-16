'''
This script contains functions to handle ISO-Country-Codes.
'''

import pycountry

from libs.kafka.logging import LogMessage

def convert_alpha_2_to_alpha_3(alpha_2_c, servicename):
    '''
    convert_alpha_2_to_alpha_3 will convert a two char. country name like DE into a three char. country like DEU.
    @param alpha_2_c will be a two char. country.
    @param servicename will be the calling service.
    @return the country name as string.
    '''
    try:
        country = pycountry.countries.get(alpha_2=alpha_2_c)
        return "Unknown" if country is None else country.alpha_3
    except Exception as error:
        LogMessage(str(error), LogMessage.LogTyp.ERROR, servicename).log()
        return "Unknown"

def convert_alpha_2_to_qualified_name(alpha_2_c, servicename):
    '''
    convert_alpha_2_to_qualified_name will convert a country name like DE to germany.
    @param alpha_2_c will be a two char. country.
    @param servicename will be the calling service.
    @return the country name as string.
    '''
    try:
        country = pycountry.countries.get(alpha_2=alpha_2_c)
        return "Unknown" if country is None else country.name
    except Exception as error:
        LogMessage(str(error), LogMessage.LogTyp.ERROR, servicename).log()
        return "Unknown"
