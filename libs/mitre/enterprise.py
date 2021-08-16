'''
This file contains functions to generate data in for mitre tactics
and techniques on an enterprise level.
'''

from pyattck import Attck

from libs.kafka.logging import LogMessage


def get_mitre_information_tactics_enterprise(tactic_list, servicename):
    '''
    get_mitre_information_tactics_enterpise will generate information about
        tacitc on an enterprise level. The information will be the same as on
        the mitre website.
    @param tactic_list will be list of tactics in the format: ['TA003',].
    @param servicename will be the name of the calling service.
    @return a dict with new and more information about a tactic. Format: {
        "TA-ID": 'TA003,
        "Title": "Some name",
        "Summary": "Some description",
        "Mitre_Link": "https://.../ta003"
    }.
    '''
    tactics = {}
    try:
        attack = Attck()
        for entry in tactic_list:
            for tactic in attack.enterprise.tactics:
                if tactic.id == entry:
                    tactics[entry] = {
                        "TA-ID": tactic.id,
                        "Title": tactic.name,
                        "Summary": tactic.description,
                        "Mitre_Link": tactic.wiki
                    }
    except Exception as error:
        LogMessage(str(error), LogMessage.LogTyp.ERROR, servicename).log()
    return tactics

def get_mitre_information_techniques_enterpise(technique_list, servicename):
    '''
    get_mitre_information_techniques_enterpise will return the information
        to an enterpise techniques.
    @param technique_list will be a list of technique-ID like T1027.
    @return will return a list with tuples containing information about
        every technique. Format: {
            "TECH-ID": 'T1123',
            "Title": "Some name",
            "Summary": "Some description",
            "Mitre_Link": technique.wiki,
            "APTs": [('APT1', 'G0003, ..), ],
            "Detections": "How_to_detect"
        }
    '''
    r_techniques = {}
    try:
        attack = Attck(nested_subtechniques=False)
        for i_technique in technique_list:
            for technique in attack.enterprise.techniques:
                if technique.id == i_technique:
                    r_techniques[i_technique] =  {
                        "TECH-ID": technique.id,
                        "Title": technique.name,
                        "Summary": technique.description,
                        "Mitre_Link": technique.wiki,
                        "APTs": [{"ID": entry.id, "Name": entry.name, "Link": entry.wiki} for entry in technique.actors],
                        "Detections": technique.detection,
                    }
    except Exception as error:
        LogMessage(str(error), LogMessage.LogTyp.ERROR, servicename).log()
    return r_techniques
