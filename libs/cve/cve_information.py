'''
This script contains functions to gather CVE information.
The informatin will be taken from CIRCL.lu
'''

import json
import requests

from libs.kafka.logging import LogMessage

CVE_URL = "https://cve.circl.lu/api/cve/{}"
EXPLOITDBLINK = "https://www.exploit-db.com/exploits/{}"

def get_cve_information(cves, servicename):
    '''
    get_cve_information will collect information about a CVE by calling ` CVE_URL ` and get
        a json reponse containing information about the CVE. After the request the method
        will extract the CVE-Score, the attack complexity, the attack vector, a summeray
        and the exploit-db-id.
    @param cves will be a list of CVE\'s in the format
        ['CVE-0000-0000', ].
    @return a dict with dicts.
    '''
    information = {}
    try:
        for entry in cves:
            response = requests.get(CVE_URL.format(entry))
            cvescore, access_com, access_vec, summary, exploitdb_link = None, None, None, None, None
            if response.status_code == 200:
                response_as_json = json.loads(response.text)
                if response_as_json is not None:
                    keys = response_as_json.keys()
                    if 'cvss' in keys:
                        cvescore = response_as_json['cvss']
                    if 'access' in keys:
                        if 'complexity' in response_as_json['access'].keys():
                            access_com = response_as_json['access']['complexity']
                        if 'vector' in response_as_json['access'].keys():
                            access_vec = response_as_json['access']['vector']
                    if 'summary' in keys:
                        summary = response_as_json['summary']
                    if 'refmap' in keys and 'exploit-db' in response_as_json['refmap'].keys():
                        exploitdb_link = EXPLOITDBLINK.format(response_as_json['refmap']['exploit-db'][0])
            information[entry] = {
                "CVS-Score": cvescore,
                "Complexity": access_com,
                "Vektor": access_vec,
                "Summary": summary,
                "Exploit-DB": exploitdb_link
            }
    except Exception as error:
        LogMessage(str(error), LogMessage.LogTyp.ERROR, servicename).log()
    return information
