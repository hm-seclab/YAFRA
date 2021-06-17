'''
This script contains functions to generate information about ips
from virustotal. This functions require a API_KEY.
'''
import time
import json
import requests

from libs.kafka.logging import LogMessage

VT_IP_ENDPOINT = 'https://www.virustotal.com/vtapi/v2/ip-address/report?apikey={}&ip={}'

#pylint: disable=R0914,R0801
def get_vt_information_ipv4(vt_api_key, ips, servicename):
    '''
    get_vt_information_ipv4 will collect information from VirusTotal about a given list
        of ipv4 adresses. After the request the method will extract the country, all
        hostnames of the ip, the number of files which are detected by an AV and the number
        of files which are not detected by an AV.
    @param ips will be a list of ips in the format ['10.10.10.10', ].
    @return will return a dict with dicts.
    '''
    information = {}
    try:
        for target in ips:
            country, hosts, detected_files, undetected_files = None, [], 0, 0
            if vt_api_key != "":
                response = requests.get(VT_IP_ENDPOINT.format(vt_api_key, target))
                if response.status_code == 204:
                    for _ in range(0,20):
                        time.sleep(30)
                        response = requests.get(VT_IP_ENDPOINT.format(vt_api_key, target))
                        if response.status_code == 200:
                            break
                if response.status_code == 200:
                    response = response.text
                    json_response = json.loads(response)
                    keys = json_response.keys()
                    if 'country' in keys: #TODO countrys missing although its in there
                        country = json_response['country']
                    if 'hostname' in keys and (list_of_hosts := [entry['hostname'] for entry in json_response['resolutions']]) is not None and len(list_of_hosts) > 0:
                        hosts = list_of_hosts
                    if 'detected_downloaded_samples' in keys and  (det_files := [entry['total'] for entry in json_response['detected_downloaded_samples']]) is not None and len(det_files) > 0:
                        detected_files = det_files[0]
                    if 'undetected_downloaded_samples' in keys and  (undet_files := [entry['total'] for entry in json_response['undetected_downloaded_samples']]) is not None and len(undet_files) > 0:
                        undetected_files = undet_files[0]
            information[target] = {
                "Country": country,
                "Hosts": hosts,
                "Detected_files": detected_files,
                "Undetected_files": undetected_files
            }
    except Exception as error:
        LogMessage(str(error), LogMessage.LogTyp.ERROR, servicename).log()
    return information
