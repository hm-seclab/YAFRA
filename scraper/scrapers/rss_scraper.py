import requests
from bs4 import BeautifulSoup

from libs.core.environment import envvar
from libs.kafka.logging import LogMessage

path_to_csv = 'resources/rss_sources.csv'

'''
Class to get RSS-Feeds by a given list.
Stores the output in a list for further use.
'''
SERVICENAME = envvar("SERVICENAME", "RssScraper")


class RssScraper:

    @staticmethod
    def get_rss_feed(url):
        try:
            soup = None
            r = requests.get(url)
            if r.status_code == 200 or r.status_code == 403:
                soup = BeautifulSoup(r.content, features='xml')

            return soup
        except Exception as error:
            LogMessage(str(error), LogMessage.LogTyp.ERROR, SERVICENAME).log()
