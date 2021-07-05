import json

import requests
from bs4 import BeautifulSoup

from libs.core.environment import envvar
from libs.kafka.logging import LogMessage

'''
Class to get data from given API Responses.
Stores the output in a list for further use.
Note -> We have to write the logic for each API different.
'''

SERVICENAME = envvar("SERVICENAME", "ApiScraper")
path_to_csv = 'resources/rss_sources.csv'
LEAKIX_API_KEY = envvar("LEAKIX", "None")


class ApiScraper:

    @staticmethod
    def get_api_response(url):

        json_list = []

        if "circl" in url:
            try:
                circl_request = requests.get(url)
                circl_content = circl_request.content
                circl_content_list = json.loads(circl_content)

                for element in circl_content_list:
                    json_list.append(element)
            except Exception as error:
                LogMessage(str(error), LogMessage.LogTyp.ERROR, SERVICENAME).log()

        elif "botvrij" in url:
            try:
                botvrij_request = requests.get(url)
                soup = BeautifulSoup(botvrij_request.text, 'html.parser')

                for link in soup.find_all('a'):
                    href = link.get('href')

                    if href.endswith('.json'):
                        link_to_json = url + "/" + href
                        link_request = requests.get(link_to_json)
                        botvrij_content = link_request.content
                        botvrij_content = json.loads(botvrij_content)
                        botvrij_content = botvrij_content["Event"]

                        json_list.append(botvrij_content)
            except Exception as error:
                LogMessage(str(error), LogMessage.LogTyp.ERROR, SERVICENAME).log()

        elif "leakix" in url:
            try:
                headers = {
                    "api-key": LEAKIX_API_KEY,
                    "Accept": "application/json"
                }

                leakix_request = requests.get(url, headers=headers)
                leakix_content = leakix_request.content
                leakix_content_list = json.loads(leakix_content)

                for element in leakix_content_list:
                    json_list.append(element)
            except Exception as error:
                LogMessage(str(error), LogMessage.LogTyp.ERROR, SERVICENAME).log()

        return json_list
