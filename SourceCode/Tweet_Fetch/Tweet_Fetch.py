'''
Developer Gowtham
Date 12 OCT 2015
'''
import tweepy
import sys

class TweetFetcher:
	def __init__(self, consumer_key, consumer_secret):
		self.consumer_key = consumer_key
		self.consumer_secret = consumer_secret
		self.auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
		self.api = tweepy.API(self.auth)

	def get_tweets(self, parsed_hashtags):
		hashtag_count = len(parsed_hashtags)
		'an implememtation to handle multiple hashtags'
		for tags in parsed_hashtags:
			return_result = self.api.search(tags)
			print tags
			for tweets in return_result:
				print tweets.text