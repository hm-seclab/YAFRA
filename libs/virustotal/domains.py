'''
This script contains functions to generate information about domains
from virustotal. This functions require a API_KEY.
'''

import time
import json
import requests

from libs.kafka.logging import LogMessage

VT_DOMAIN_ENDPOINT = 'https://www.virustotal.com/vtapi/v2/domain/report?apikey={}&domain={}'

#pylint: disable=R0914,R0801
def get_vt_information_domains(vt_api_key, domains, servicename):
    '''
    get_vt_information_domains will collect information from VirusTotal about a given list
        of ipv4 adresses. After the request the method will extract the subdomains, sibbling_domains
        sophos category, resolutions (hosts of the domain), detected_files and undetected_files.
    @param vt_api_key will be the virustotal apikey.
    @param domains will be a list of domains.
    @param servicename will be the name of the calling serivce.
    @return a dict with the new information. Format: {
                "Possible_subdomains": ['x.domain.com', ],
                "Sibbling_domains": ['domain.de', 'domain.net'],
                "Categories": 'Malware ..',
                "IPs": ['129.232.2.2', '12.9.23.22'],
                "Detected_files": detected_files,
                "Undetected_files": undetected_files
            }
    '''
    information = {}
    av_cats = ['sophos category', 'Forcepoint ThreatSeeker category', 'Webroot category', 'alphaMountain.ai category', 'Comodo Valkyrie Verdict category', 'Dr.Web category', 'BitDefender domain info']
    forbidden_cats = ['uncategorized', 'Unrated', 'unknown']
    try:
        for target in domains:
            response = requests.get(VT_DOMAIN_ENDPOINT.format(vt_api_key, target))
            prob_subdomain, sibbling_domains, domain_categories, domains_ips, detected_files, undetected_files, vendor = [], [], "Unknown", [], 0, 0, "-"
            if response.status_code == 204:
                for _ in range(0,20):
                    time.sleep(30)
                    response = requests.get(VT_DOMAIN_ENDPOINT.format(vt_api_key, target))
                    if response.status_code == 200:
                        break
            if response.status_code == 200:
                response = response.text
                json_response = json.loads(response)
                keys = json_response.keys()
                if 'subdomains' in keys and (subdomains := json_response['subdomains']) is not None and len(subdomains) > 0:
                    prob_subdomain = subdomains
                if 'domain_siblings' in keys and (sibblings := json_response['domain_siblings']) is not None and len(sibblings) > 0:
                    sibbling_domains = sibblings
                for cat in av_cats:
                    if cat in keys and (categories := json_response[cat]) is not None and categories not in forbidden_cats and domain_categories == "Unknown":
                        domain_categories, vendor = categories, cat
                if domain_categories is None and 'sophos category' in keys and (categories := json_response['sophos category']) is not None:
                    domain_categories = categories
                if 'resolutions' in keys and (ips := [entry['ip_address'] for entry in json_response['resolutions']]) is not None and len(ips) > 0:
                    domains_ips = ips
                if 'detected_downloaded_samples' in keys and (det_files := [entry['total'] for entry in json_response['detected_downloaded_samples']]) is not None and len(det_files) > 0:
                    detected_files = det_files[0]
                if 'undetected_downloaded_samples' in keys and (undet_files := [entry['total'] for entry in json_response['undetected_downloaded_samples']]) is not None and len(undet_files) > 0:
                    undetected_files = undet_files[0]
            information[target] = {
                "Possible_subdomains": prob_subdomain,
                "Sibbling_domains": sibbling_domains,
                "Categories": domain_categories,
                "IPs": domains_ips,
                "Detected_files": detected_files,
                "Undetected_files": undetected_files,
                "Vendor": vendor
            }
    except Exception as error:
        LogMessage(str(error), LogMessage.LogTyp.ERROR, servicename).log()
    return information
