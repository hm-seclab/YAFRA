import tweepy
import os
from dotenv import load_dotenv

from libs.core.environment import envvar
from libs.kafka.logging import LogMessage

load_dotenv()

'''
Class to get tweets for a list of given users.
Stores the output in a list for further use.
'''
SERVICENAME = envvar("SERVICENAME", "TwitterScraper")
auth = tweepy.OAuthHandler(os.environ.get('TWITTER_CONSUMER_KEY'), os.environ.get('TWITTER_CONSUMER_KEY_SECRET'))
auth.set_access_token(os.environ.get('TWITTER_ACCESS_TOKEN'), os.environ.get('TWITTER_ACCESS_TOKEN_SECRET'))

api = tweepy.API(auth)


class TwitterScraper:

    @staticmethod
    def get_twitter_feed(twitter_user):

        twitter_feed_list = []

        try:
            tweets = api.user_timeline(screen_name=twitter_user,
                                       # 200 is the maximum allowed count
                                       count=200,
                                       include_rts=False,
                                       # Necessary to keep full_text
                                       # otherwise only the first 140 words are extracted
                                       tweet_mode='extended'
                                       )
            # gets the latest 300 tweets
            for info in tweets[:int(os.environ.get('TWEET_COUNT'))]:
                if info is not None:
                    twitter_feed_list.append(info)

            return twitter_feed_list
        except Exception as error:
            LogMessage(str(error), LogMessage.LogTyp.ERROR, SERVICENAME).log()
