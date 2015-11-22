import logging
logging.basicConfig(filename='tweet.log', level=logging.INFO, format='%(asctime)s %(message)s')

from Tweet_Fetch import *
from TweetViz_Hashtag_Generator import TweetVizHashTagGenerator
from TweetViz_DataStorageReader import TweetVizDataStorageReader
import sys

consumer_key = 'WQGD1vxJe2COJntOcbq1L7ydH'
consumer_secret = 'O6MiuVHUpAgHwBEpsOyzSSfNMvIFdsAX0xhmOrmhKmrDnzxYUo'


def main_fun(user_text):
    logging.debug("Entered main function")

    # 'collects hashtag without hash'
    # Finalhashtags = []
    # sentence = ""
    # sentence = "Trump vs Sanders"
    # sentence = "Windows vs Linux vs Mac"
    # sentence = "Modi vs Rahul"
    # sentence = "India vs China"
    sentence = ''
    if user_text is not None and user_text.__len__() > 0:
        sentence = user_text
        print('User argument got - ' + user_text.__str__())
    else:
        #sentence = 'Windows10 vs OSXElCapitan'
        sentence = 'Sundevils vs Wildcats'
        print('Did not get user argument taking default- '+sentence)

    data_handler = TweetVizDataStorageReader()
    data_handler.read_configuration_file()

    '''
    CRITICAL = 50
    FATAL = CRITICAL
    ERROR = 40
    WARNING = 30
    WARN = WARNING
    INFO = 20
    DEBUG = 10
    NOTSET = 0
    '''

    if data_handler.Log_Level == 0:
        logging.getLogger().setLevel(logging.INFO)
    elif data_handler.Log_Level == 40:
        logging.getLogger().setLevel(logging.ERROR)
    elif data_handler.Log_Level == 30:
        logging.getLogger().setLevel(logging.WARNING)
    elif data_handler.Log_Level == 20:
        logging.getLogger().setLevel(logging.INFO)
    elif data_handler.Log_Level == 10:
        logging.getLogger().setLevel(logging.DEBUG)
    else:
        logging.getLogger().setLevel(logging.INFO)


    logging.info("Hashtag mentioned %s", sentence)
    hashtagsgen = TweetVizHashTagGenerator()
    hashtagsgen.user_statement = sentence
    hashtags = hashtagsgen.hash_tag_generator()

    print(sentence)
    print(hashtags)


    # 'create an object of Tweet_Fetch class and instantiate the variables'
    tweet_fetcher = TweetFetcher(consumer_key, consumer_secret)
    tweet_fetcher.No_Of_Tweets_Fetch = data_handler.Number_Of_Tweets
    if tweet_fetcher.No_Of_Tweets_Fetch != data_handler.Number_Of_Tweets:
        tweet_fetcher._No_Of_Tweets_to_fetch = data_handler.Number_Of_Tweets

    tweet_fetcher.Type_Of_Tweets = data_handler.Type_Of_Tweets

    tweet_table = tweet_fetcher.get_tweets(hashtags, sentence)
    # print(tweet_table)
    # logging.info('Tweet table %s', tweet_table)


    data_handler.write_to_file(tweet_table)
    table_temp = data_handler.read_from_file()

    if not data_handler.File_Mode:
        data_handler.insert_data_to_db(tweet_table)
        table_temp = data_handler.read_full_details_from_db()

    logging.debug("Leaving main function")
    print('Finished application......')

    pass


if __name__ == '__main__':

    user_argument = ''
    if sys.argv.__len__() > 1:
        user_argument = sys.argv[1]
    main_fun(user_argument)
