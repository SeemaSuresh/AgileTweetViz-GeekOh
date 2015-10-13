from Tweet_Fetch import *
from TweetViz_Hashtag_Generator import TweetVizHashTagGenerator

consumer_key = 'WQGD1vxJe2COJntOcbq1L7ydH'
consumer_secret = 'O6MiuVHUpAgHwBEpsOyzSSfNMvIFdsAX0xhmOrmhKmrDnzxYUo'


def main_fun():
    # 'collects hashtag without hash'
    Finalhashtags = []
    sentence = "SunDevil is awesome"
    hashtagsgen = TweetVizHashTagGenerator()
    hashtagsgen.user_statement = sentence
    hashtags = hashtagsgen.hash_tag_generator()

    for hashtag in hashtags:
        string_hashtag = '#' + str(hashtag)
        Finalhashtags.append(string_hashtag)
    # 'create an object of Tweet_Fetch class and instantiate the variables'
    tweet_fetcher = TweetFetcher(consumer_key, consumer_secret)
    print(tweet_fetcher.get_tweets(Finalhashtags))
    pass


if __name__ == '__main__':
    main_fun()
