Feature: Scraper Microservice
  As a security analyst,
  I want to get scraped data from twitter, rss-feeds and apis.
  To push the data in an appropriate format to a kafka topic.

  Scenario Outline: Basic Scraper Logic
    Given the scraper with prepared sources to collect data from
    When the scraper successfully collects data from valid sources
    Examples:
      |  |
