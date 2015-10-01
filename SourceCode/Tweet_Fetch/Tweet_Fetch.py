import tweepy

consumer_key = 'WQGD1vxJe2COJntOcbq1L7ydH'
consumer_secret = 'O6MiuVHUpAgHwBEpsOyzSSfNMvIFdsAX0xhmOrmhKmrDnzxYUo'

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_key, access_secret)

api = tweepy.API(auth)

return_result = api.search("#asu")

for results in return_result:
	print results.text
#public_tweets = api.home_timeline()

#user = api.get_user('gowthamnayak7')
#print user.followers_count

#for friend in user.friends():
#	print friend.screen_name
#for tweet in public_tweets:
#	print tweet.text