"""
This module contains step definitions for scraper.feature.
"""
import json
from unittest.mock import patch

import pytest
from kafka import KafkaProducer

from pytest_bdd import scenarios, when, given

from libs.core.get_path import get_path
from libs.kafka.logging import LogMessage
from scraper.core.server import Scraper

from scraper.scrapers.api_scraper import ApiScraper
from scraper.scrapers.rss_scraper import RssScraper
from scraper.scrapers.twitter_scraper import TwitterScraper

scenarios('../features/scraper.feature')


@pytest.fixture
def scraper():
    scraper = Scraper()
    yield scraper


@given("the scraper with prepared sources to collect data from")
def scraper_get_sources(scraper):

    with patch.object(LogMessage, 'log'), patch('os.path.abspath') as mocked_resources:
        mocked_resources.return_value = './scraper/tests_integration_scraper/step_defs/resources/mocked_resources.json'
        scraper.refetch_sources()


@when("the scraper successfully collects data from valid sources")
def scraper_successful_data_collection(scraper):
    rss_path = get_path(__file__, 'resources/rss_response.txt')
    twitter_path = get_path(__file__, 'resources/twitter_response.json')
    api_path = get_path(__file__, 'resources/api_response.json')

    with open(str(rss_path)) as rss_file, open(str(twitter_path)) as twitter_file, open(str(api_path)) as api_file:
        rss_data = rss_file.read()
        twitter_data = json.load(twitter_file)
        twitter_data = json.dumps(twitter_data)
        api_data = json.load(api_file)
        api_data = json.dumps(api_data)

    with patch.object(KafkaProducer, 'send') as mock_push_collected_data, \
            patch.object(RssScraper, 'get_rss_feed') as mocked_rss_data, \
            patch.object(TwitterScraper, 'get_twitter_feed') as mocked_twitter_data, \
            patch.object(ApiScraper, 'get_api_response') as mocked_api_data:
        mocked_rss_data.return_value = str(rss_data)
        mocked_twitter_data.return_value = str(twitter_data)
        mocked_api_data.return_value = str(api_data)
        scraper.collect_data_from_sources()
        mock_push_collected_data.assert_called()
