from Tweet_Fetch import *
from TweetViz_Hashtag_Generator import TweetVizHashTagGenerator
from TweetViz_DataStorageReader import TweetVizDataStorageReader

consumer_key = 'WQGD1vxJe2COJntOcbq1L7ydH'
consumer_secret = 'O6MiuVHUpAgHwBEpsOyzSSfNMvIFdsAX0xhmOrmhKmrDnzxYUo'


def main_fun():
    # 'collects hashtag without hash'
    # Finalhashtags = []
    sentence = "Windows10 vs OSXElCapitan"
    hashtagsgen = TweetVizHashTagGenerator()
    hashtagsgen.user_statement = sentence
    hashtags = hashtagsgen.hash_tag_generator()


    # 'create an object of Tweet_Fetch class and instantiate the variables'
    tweet_fetcher = TweetFetcher(consumer_key, consumer_secret)
    tweet_table = tweet_fetcher.get_tweets(hashtags, sentence)
    print(tweet_table)

    data_handler = TweetVizDataStorageReader()
    data_handler.read_configuration_file()
    data_handler.write_to_file(tweet_table)
    pass


if __name__ == '__main__':
    main_fun()
