from User import *
from Location import *

class Tweet(object):
    def __init__(hashtag, twitter_handle, tweet_message, tweet_creation_time, tweet_location, tweet_retweet_count, tweet_favorite_count):
    	self.hashtag = hashtag
    	self.user = twitter_handle
    	self.tweet_text = tweet_text
    	self.date = tweet_creation_time
    	self.coordinates = tweet_location
    	self.favorite_count = tweet_favorite_count
        self.retweet_count = tweet_retweet_count