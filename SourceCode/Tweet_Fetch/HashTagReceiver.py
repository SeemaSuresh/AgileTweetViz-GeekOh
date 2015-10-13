import sys
from Tweet_Fetch import *

consumer_key = 'WQGD1vxJe2COJntOcbq1L7ydH'
consumer_secret = 'O6MiuVHUpAgHwBEpsOyzSSfNMvIFdsAX0xhmOrmhKmrDnzxYUo'

def main_fun():
	'collects hashtag without hash'
	hashtags = []
	index = 0
	for hashtag in sys.argv[1:]:
		string_hashtag = '#' + str(hashtag)
		hashtags.append(string_hashtag)

	'create an object of Tweet_Fetch class and instantiate the variables'
	tweet_fetcher = TweetFetcher(consumer_key, consumer_secret)
	tweet_fetcher.get_tweets(hashtags)

main_fun()