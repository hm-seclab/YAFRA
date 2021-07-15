import tweepy

from libs.core.environment import envvar
from libs.kafka.logging import LogMessage

'''
Class to get tweets for a list of given users.
Stores the output in a list for further use.
'''
SERVICENAME = envvar("SERVICENAME", "TwitterScraper")
TWITTER_CONSUMER_KEY = envvar("TWITTER_CONSUMER_KEY", "None")
TWITTER_CONSUMER_KEY_SECRET = envvar("TWITTER_CONSUMER_KEY_SECRET", "None")
TWITTER_ACCESS_TOKEN = envvar("TWITTER_ACCESS_TOKEN", "None")
TWITTER_ACCESS_TOKEN_SECRET = envvar("TWITTER_ACCESS_TOKEN_SECRET", "None")
TWEET_COUNT = envvar("TWEET_COUNT", "None")

auth = tweepy.OAuthHandler(TWITTER_CONSUMER_KEY, TWITTER_CONSUMER_KEY_SECRET)
auth.set_access_token(TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_TOKEN_SECRET)

api = tweepy.API(auth)


class TwitterScraper:

    @staticmethod
    def get_twitter_feed(twitter_user):
        '''
        get_twitter_feed is scraping the tweets for a given twitter user.
        @param twitter_user will be the twitter user, which tweets got scraped.
        @return twitter_feed_list will return a list of all scraped tweets of a twitter user.
        '''
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
            for info in tweets[:int(TWEET_COUNT)]:
                if info is not None:
                    twitter_feed_list.append(info)
        except Exception as error:
            LogMessage(str(error), LogMessage.LogTyp.ERROR, SERVICENAME).log()
        return twitter_feed_list
