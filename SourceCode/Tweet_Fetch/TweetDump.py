'''
http://stackoverflow.com/questions/30362651/getting-tweets-by-date-with-tweepy
'''
'''
Developer Gowtham
Date 12 OCT 2015
reference - http://stackoverflow.com/questions/22469713/managing-tweepy-api-search
            https://nawarkhede.wordpress.com/2014/08/16/separating-tweets-from-text-image-videos-using-tweepy-python/
            http://www.benkhalifa.com/twitter-crawler-python
'''
import tweepy
import logging
from geopy import geocoders
from datetime import date, datetime, time

logging.basicConfig(filename='tweet.log', level=logging.INFO, format='%(asctime)s %(message)s')


class TweetFetcher:
    def __init__(self, consumer_key, consumer_secret):
        self.consumer_key = consumer_key
        self.consumer_secret = consumer_secret
        self.auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        self.api = tweepy.API(self.auth)
        self._No_Of_Tweets_to_fetch = 1000


    def get_tweets(self, parsed_hashtags, search_sentence):
        logging.debug("entered get_tweets")

        file_object = open(str(datetime.now().date()) + '.txt', "wb")

        for tags in parsed_hashtags:
            hash_tweets = self.fetch_tweets(tags)
            for tweets in hash_tweets:
                file_object.write(tweets)
        file_object.close()
        return

    def fetch_tweets(self, hashtag):
        page = 1
        deadend = False
        tweet_list = []

        while True:
            tweets = self.api.search(q=hashtag, result_type="mixed", lang="en")

            for tweet in tweets:
                if (datetime.now() - tweet.created_at).days < 1:
                    logging.debug("Enter for loop")
                    if not tweet.text.encode('utf-8').startswith('RT'):
                        logging.debug("Accept if condition for checking re tweets")
                        if tweet.entities.__contains__('media') and tweet.entities['media'][0]['type'] == 'photo':
                            logging.debug("Checking for photos in tweet")
                            continue

                    tweet_list.append(tweet.text.encode("utf-8"))
                else:
                    deadend = True
                    return tweet_list
            if not deadend:
                page+=1
                time.sleep(500)

consumer_key = 'WQGD1vxJe2COJntOcbq1L7ydH'
consumer_secret = 'O6MiuVHUpAgHwBEpsOyzSSfNMvIFdsAX0xhmOrmhKmrDnzxYUo'
tf = TweetFetcher(consumer_key, consumer_secret)
tf.get_tweets(["#asu"], "asu is a good college")