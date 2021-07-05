'''
This class will represent the reporter-server.
'''

# pylint: disable=C0413, C0411
import datetime
import json
import sys
from threading import Thread

import pytz
from kafka import KafkaProducer

from libs.kafka.topichandler import create_topic_if_not_exists
from scraper.core.static.DataObject import DataObject
from scraper.scrapers.api_scraper import ApiScraper
from scraper.scrapers.rss_scraper import RssScraper
from scraper.scrapers.twitter_scraper import TwitterScraper

sys.path.append('..')

from flask import Flask
from flask_script import Server
from flask_apscheduler import APScheduler

from libs.core.environment import envvar
from libs.kafka.logging import LogMessage
from libs.kafka.logging import send_health_message

SERVICENAME = envvar("SERVICENAME", "Scraper")
KAFKA_SERVER = envvar("KAFKA_SERVER", "0.0.0.0:9092")
SCRAPER_TOPIC_NAME = envvar("SCRAPER_TOPIC", "scraper")
HEALTHTOPIC = envvar("HEALTH_TOPIC", "health_report")
MISP_SERVER = envvar("MISP_SERVER", "0.0.0.0")
MISP_TOKEN = envvar("MISP_TOKEN", None)
MISP_CERT_VERIFY = True if envvar("MISP_VERIF", True) == "True" else False

CSV_BASE_PATH = '../scrapers/resources/'

RSS_FEED_CSV_PATH = CSV_BASE_PATH + 'rss_sources.csv'
TWITTER_FEED_CSV_PATH = CSV_BASE_PATH + 'twitter_sources.csv'
API_CSV_PATH = CSV_BASE_PATH + 'api_sources.csv'


class Config:
    '''
    Config class with configs for flask.
    '''
    SCHEDULER_API_ENABLED = True


app = Flask(SERVICENAME)
app.config.from_object(Config())

scheduler = APScheduler()
scheduler.init_app(app)


class Scraper(Server):
    '''
    Scraper will be a class representing the scraper-service.
    '''

    @scheduler.task("interval", id="health_push", seconds=5, timezone=pytz.UTC)
    def healthpush():
        '''
        healthpush will send a health message to KAFKA.
        '''
        try:
            send_health_message(KAFKA_SERVER, HEALTHTOPIC, SERVICENAME)
        except Exception as error:
            LogMessage(str(error), LogMessage.LogTyp.ERROR, SERVICENAME).log()

    @staticmethod
    def collect_data_from_sources():
        '''
        collect_data_from_sources starts the collection process by scraping data from various given sources.
        '''
        try:
            rss_data = Scraper.__get_data_from_rss_feed()
            twitter_data = Scraper.__get_data_from_twitter_feed()
            api_data = Scraper.__get_data_from_api()

            data_list = rss_data + twitter_data + api_data

            for data in data_list:
                data_as_json = json.dumps(data.__dict__, default=Scraper.__datetime_converter)
                Scraper.push_collected_data(data_as_json)
        except Exception as error:
            LogMessage(str(error), LogMessage.LogTyp.ERROR, SERVICENAME).log()

    @staticmethod
    def __get_data_from_rss_feed():
        '''
        __get_data_from_rss_feed scrapes all the given rss-feeds and stores them properly for further usage.
        '''
        try:
            print("Stepping into __get_data_from_rss_feed")

            rss_scraper = RssScraper
            url_list = Scraper.__load_csv_sources(RSS_FEED_CSV_PATH)
            ret_val_list = []

            for url in url_list:
                rss_feed = rss_scraper.get_rss_feed(url)

                if not rss_feed:
                    continue

                rss_feed_item_list = rss_feed.findAll('item')

                for rss_feed_item in rss_feed_item_list:

                    if rss_feed_item is None:
                        continue

                    content = rss_feed_item.text

                    if content is None:
                        continue

                    item_title = rss_feed_item.find('title')

                    # Change the url, when using it inside the title to avoid path conflicts
                    title_url = url

                    if str(url).startswith("http://"):
                        title_url = url.replace("http://", "")

                    if str(url).startswith("https://"):
                        title_url = url.replace("https://", "")

                    if item_title is None:
                        item_title = "_no_item_title"
                    else:
                        item_title = str(item_title).strip("<title> </title>")

                    publication_date = rss_feed_item.find('pubDate')

                    if publication_date is None:
                        date = "no_date"
                    else:
                        date = publication_date.text

                    title = "rss_" + str(item_title) + "_" + str(title_url) + "_" + str(date)
                    data_object = DataObject(content, title, url, date)
                    ret_val_list.append(data_object)

            print("Stepping out __get_data_from_rss_feed. Found " + str(len(ret_val_list)) + " rss-feeds.")
            return ret_val_list
        except Exception as error:
            LogMessage(str(error), LogMessage.LogTyp.ERROR, SERVICENAME).log()

    @staticmethod
    def __get_data_from_twitter_feed():
        '''
        __get_data_from_twitter_feed scrapes all the given tweets and stores them properly for further usage.
        '''

        try:
            print("Stepping into __get_data_from_twitter_feed")

            twitter_scraper = TwitterScraper
            twitter_user_list = Scraper.__load_csv_sources(TWITTER_FEED_CSV_PATH)
            ret_val_list = []

            for twitter_user in twitter_user_list:

                twitter_feed_list = twitter_scraper.get_twitter_feed(twitter_user)

                if not twitter_feed_list:
                    continue

                for tweet in twitter_feed_list:

                    if tweet is None:
                        continue

                    publication_date = tweet.created_at

                    if publication_date is None:
                        date = "no_date"
                    else:
                        date = publication_date

                    title = "twitter_" + str(twitter_user) + "_" + str(date)

                    data_object = DataObject(tweet.full_text, title, str(twitter_user), date)
                    ret_val_list.append(data_object)

            print("Stepping out __get_data_from_twitter_feed. Found " + str(len(ret_val_list)) + " tweets.")
            return ret_val_list
        except Exception as error:
            LogMessage(str(error), LogMessage.LogTyp.ERROR, SERVICENAME).log()

    @staticmethod
    def __get_data_from_api():
        '''
        __get_data_from_api scrapes all the given apis and stores the responses properly for further usage.
        '''
        try:
            print("Stepping into __get_data_from_api")

            api_scraper = ApiScraper
            url_list = Scraper.__load_csv_sources(API_CSV_PATH)
            ret_val_list = []

            for url in url_list:
                api_response_list = api_scraper.get_api_response(url)

                if not api_response_list:
                    continue

                for api_response in api_response_list:

                    if api_response is None:
                        continue

                    date = "no_date"

                    if "Published" in api_response:
                        date = api_response["Published"]

                    if "publish_timestamp" in api_response:
                        date = api_response["publish_timestamp"]

                    if "time" in api_response:
                        date = api_response["time"]

                    title_url = url

                    if str(url).startswith("http://"):
                        title_url = url.replace("http://", "")

                    if str(url).startswith("https://"):
                        title_url = url.replace("https://", "")

                    title = "api_" + str(title_url) + "_" + str(date)

                    data_object = DataObject(api_response, title, url, date)
                    ret_val_list.append(data_object)

            print("Stepping out __get_data_from_api. Found " + str(len(ret_val_list)) + " api responses.")
            return ret_val_list
        except Exception as error:
            LogMessage(str(error), LogMessage.LogTyp.ERROR, SERVICENAME).log()

    @staticmethod
    def __datetime_converter(o):
        '''
        helper method for converting the datetime
        '''
        if isinstance(o, datetime.datetime):
            return o.__str__()

    @staticmethod
    def push_collected_data(data):
        '''
        push_collected_data will push all collected data to KAFKA.
        @param data will be the data.
        '''
        try:
            producer = KafkaProducer(bootstrap_servers=KAFKA_SERVER, client_id='scraper', api_version=(2, 7, 0))
            message = str(data)
            producer.send(SCRAPER_TOPIC_NAME, message)
        except Exception as error:
            LogMessage(str(error), LogMessage.LogTyp.ERROR, SERVICENAME).log()

    @staticmethod
    def __load_csv_sources(path_to_csv):
        '''
        __load_csv_sources is a helper method to load the relevant
        csv sources, which are necessary to scrape the data from.
        @param path_to_csv path to the csv file.
        '''
        try:
            csv_list = []

            with open(path_to_csv, 'r') as f:
                for line in f.readlines():
                    l = line.strip()
                    csv_list.append(l)

            return csv_list

        except Exception as error:
            LogMessage(str(error), LogMessage.LogTyp.ERROR, SERVICENAME).log()

    def __call__(self, app, *args, **kwargs):
        '''
        __call__ override __call__ function from server-class.
        '''
        create_topic_if_not_exists(KAFKA_SERVER, SCRAPER_TOPIC_NAME)
        scheduler.start()
        Thread(target=Scraper.collect_data_from_sources(), daemon=True).start()
        return Server.__call__(self, app, *args, **kwargs)