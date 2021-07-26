'''
This script contains functions to handle and interact with misp.
'''

from pymisp import MISPEvent
from pymisp import MISPObject

from collections import ChainMap

from libs.kafka.logging import LogMessage
from libs.extensions.loader import load_extensions
from libs.extensions.loader import append_extensions_misp_types

MISP_MAP = {
    "Autonomous system": "AS",
    "Overview": "comment",
    "Traffic Light Protocol": "comment",
    "Emails": "email",
    "Bitcoin": "btc",
    "URLs": 'url',
    "URL": 'url',
    "MD5": 'md5',
    "SHA-256": 'sha256',
    "SHA-512": 'sha512',
    "SHA-1": 'sha1',
    "Filenames": 'filename',
    'Filepaths': 'filename',
    "Registry Keys": "regkey",
    'CVE': 'vulnerability',
    'Githubrepositorys': 'github-repository',
    'Githubaccounts': 'github-username',
    'HTTP Requests': 'http-method',
    'SSDeeps': 'ssdeep'
}

EXTENSIONS = load_extensions("Library")

MISP_MAP = append_extensions_misp_types(MISP_MAP, EXTENSIONS, "Library")

def get_misp_type(keyname):
    '''
    get_misp_type will return the type of the misp_attribute.
    @param keyname will be the name of the attribute like domains.
    @return the type as string.
    '''
    msip_type = "other"
    try:
        if keyname in MISP_MAP.keys():
            msip_type = MISP_MAP[str(keyname)]
    except Exception:
        pass
    return msip_type

def create_misp_event(servicename, distribution=0, threat_level_id=4, publish=False, analysis=0, event_info=None):
    '''
    create_misp_event will add a new misp event.
    @param distribution will be the misp visibility level.
    @param threat_level will be the misp threat-level.
    @param publish will be a boolean indecating whether or not the report
        should be released.
    @param analysis will be something like initial, ongoing, completed.
    @param event_info will be additional information about the event.
    @param servicename will be the name of the calling service.
    '''
    event = None
    try:
        event = MISPEvent()
        event.distribution = int(distribution) if 0 <= distribution <= 3 else 0
        event.threat_level_id = int(threat_level_id) if 1 <= threat_level_id <= 4 else 4
        event.analysis = int(analysis) if 0 <= analysis <= 2 else 0
        event.info = event_info if event_info is not None else "-"
        if publish:
            event.publish()
    except Exception as error:
        LogMessage(str(error), LogMessage.LogTyp.ERROR, servicename).log()
    return event

def object_to_string(obj, servicename):
    '''
    object_to_string will turn an object into a string but
        prettified for misp.prettifyed
    @param obj will be the object to stringify.
    @return the object as string.
    @param servicename will be the name of the calling service.
    '''
    string = ""
    try:
        for key, value in obj.items():
            string += "{}: {} \n".format(key, value, servicename)
    except Exception as error:
        LogMessage(str(error), LogMessage.LogTyp.ERROR, servicename).log()
    return string

def handle_object_input(event, obj, parent_key, servicename):
    '''
    handle_object_input will handle a object/dict as attribute values of the event.
    @param event will be the misp event the list should be added to.
    @param liste will be the list to add.
    @param parent_key will be the name of the parent category.
    @param servicename will be the name of the calling service.
    '''
    try:
        for key, value in obj.items():
            if isinstance(value, list):
                handle_list_input(event, value, key, servicename)
            elif isinstance(value, dict):
                handle_object_input(event, value, key, servicename)
            else:
                try:
                    if not parent_key.startswith("CVE-") and not "Domains" in obj.keys() and not "Domain" in obj.keys() and parent_key != "IPv4-Address":
                        if 'Related Events' in obj.keys():
                            event.add_attribute(get_misp_type(key), value)
                        else:
                            event.add_attribute(get_misp_type(parent_key), object_to_string(obj, servicename))
                        continue
                    else:
                        return
                except Exception as error:
                    LogMessage(str(error), LogMessage.LogTyp.ERROR, servicename).log()
    except Exception as error:
        LogMessage(str(error), LogMessage.LogTyp.ERROR, servicename).log()

def handle_list_input(event, liste, parent_key, servicename):
    '''
    handle_list_input will handle a list as attribute values of the event.
    @param event will be the misp event the list should be added to.
    @param liste will be the list to add.
    @param parent_key will be the name of the parent category.
    @param servicename will be the name of the calling service.
    '''
    try:
        for element in liste:
            if isinstance(element, dict):
                handle_object_input(event, element, parent_key, servicename)
            else:
                try:
                    event.add_attribute(get_misp_type(parent_key), element)
                except Exception as error:
                    LogMessage(str(error), LogMessage.LogTyp.ERROR, servicename).log()
    except Exception as error:
        LogMessage(str(error), LogMessage.LogTyp.ERROR, servicename).log()

def traverse_findings(event, findings, servicename):
    '''
    traverse_findings will recursively walk throw the dict
        and call the appropriate handler.
    @param event will be a misp-event which should get an attribute.
    @param findings will be a dict with all findings.
    @param servicename will be the name of the calling service.
    '''
    try:
        for key, value in findings['data'].items():
            if isinstance(value, dict):
                handle_object_input(event, value, key, servicename)
            elif isinstance(value, list):
                handle_list_input(event, value, key, servicename)
            else:
                try:
                    event.add_attribute(get_misp_type(key), str(value))
                except Exception as error:
                    LogMessage(str(error), LogMessage.LogTyp.ERROR, servicename).log()
    except Exception as error:
        LogMessage(str(error), LogMessage.LogTyp.ERROR, servicename).log()


def handle_cve_object(event, obj, vuln_id, misp, servicename):
    '''
    handle_cve_object will create an cve object in misp.
    @param event will be a misp-event which should get an attribute.
    @param obj will be a dict with all info.
    @param obj will be the id of the CVE.
    @param misp will be a handle to the misp plattfrom.
    @param servicename will be the name of the calling service.
    '''
    try:
        obj = ChainMap(*obj)
        cve_object = MISPObject('vulnerability', standalone=False)
        data = {
                'cvss-score': obj['CVS-Score'], 
                'cvss-string': "{}/{}".format(obj['Complexity'], obj['Vektor']),
                'summary': obj['text'],
                'references': 'https://cve.mitre.org/cgi-bin/cvename.cgi?name={}'.format(vuln_id),
                'id': vuln_id,
            }
        for key, value in data.items(): cve_object.add_attribute(key, value)
        misp.add_object(event, cve_object)
    except Exception as error:
        LogMessage(str(error), LogMessage.LogTyp.ERROR, servicename).log()

def handle_domain_object(event, obj, misp, servicename):
    '''
    handle_domain_object will create an domain object in misp.
    @param event will be a misp-event which should get an attribute.
    @param obj will be a dict with all info.
    @param misp will be a handle to the misp plattfrom.
    @param servicename will be the name of the calling service.
    '''
    try:
        domain_object = MISPObject('domain-ip', standalone=False)
        data = {
                'domain': obj['Domain'], 
                'text': obj['Categories'],
            }
        for key, value in data.items(): domain_object.add_attribute(key, value)
        misp.add_object(event, domain_object)
    except Exception as error:
        LogMessage(str(error), LogMessage.LogTyp.ERROR, servicename).log()

def handle_ip_object(event, obj, misp, servicename):
    '''
    handle_ip_object will create an ip object in misp.
    @param event will be a misp-event which should get an attribute.
    @param obj will be a dict with all info.
    @param misp will be a handle to the misp plattfrom.
    @param servicename will be the name of the calling service.
    '''
    try:
        t = MISPObject('ip-port', standalone=False)
        data = {
                'ip-dst': obj['IP'], 
                'text': obj['Country'],
            }
        for key, value in data.items():
            t.add_attribute(key, value)
        misp.add_object(event, t)
    except Exception as error:
        LogMessage(str(error), LogMessage.LogTyp.ERROR, servicename).log()


def handle_misp_event(misp, findings, servicename):
    '''
    handle_misp_event will create an event and put in
        all findings as attributes.
    @param findings will be a dict with all findings.
    @param misp will a handle to the misp-plattform.
    @param servicename will be the name of the calling service.
    '''
    try:
        eventname = findings["Eventname"] if "Eventname" in findings.keys() and findings["Eventname"] is not None else "No title"
        if (event := create_misp_event(event_info=eventname, servicename=servicename)) is not None:
            traverse_findings(event, findings, servicename)
            misp.add_event(event)
            f_keys = findings['data'].keys()
            if 'CVEs' in f_keys and findings['data']['CVEs'] is not None:
                for key, value in findings['data']['CVEs'].items():
                    handle_cve_object(event, value, key, misp, servicename)
            if 'Network' in f_keys and (net_keys := findings['data']['Network']) is not None:
                if 'Domains' in net_keys and findings['data']['Network']['Domains'] is not None:
                    for domain in findings['data']['Network']['Domains']:
                        handle_domain_object(event, domain, misp, servicename)
                if 'IPv4 and IPv6' in net_keys and (ip_keys := findings['data']['Network']['IPv4 and IPv6'].keys()) is not None and 'IPv4-Address' in ip_keys:        
                    for ip in findings['data']['Network']['IPv4 and IPv6']['IPv4-Address']:
                        handle_ip_object(event, ip, misp, servicename)
            if findings['data'] and len(findings['data']) > 0:
                event.publish()
        else:
            LogMessage("Cannot get an event.", LogMessage.LogTyp.ERROR, servicename).log()
    except Exception as error:
        LogMessage(str(error), LogMessage.LogTyp.ERROR, servicename).log()
