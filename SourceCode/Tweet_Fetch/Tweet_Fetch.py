'''
Developer Gowtham
Date 12 OCT 2015
reference - http://stackoverflow.com/questions/22469713/managing-tweepy-api-search
            https://nawarkhede.wordpress.com/2014/08/16/separating-tweets-from-text-image-videos-using-tweepy-python/
            http://www.benkhalifa.com/twitter-crawler-python
'''
import tweepy
import logging
logging.basicConfig(filename='tweet.log', level=logging.INFO, format='%(asctime)s %(message)s')
from geopy import geocoders


class TweetFetcher:
    def __init__(self, consumer_key, consumer_secret):
        self.consumer_key = consumer_key
        self.consumer_secret = consumer_secret
        self.auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        self.api = tweepy.API(self.auth)

    def get_tweets(self, parsed_hashtags, search_sentence):
        logging.debug("entered get_tweets")
        # hashtag_count = len(parsed_hashtags)
        # 'an implememtation to handle multiple hashtags'

        table_data = []
        logging.info("Table data %s", table_data)
        max_tweets = 100*parsed_hashtags.__len__()

        for tags in parsed_hashtags:
            logging.debug("Enter for loop")
            # return_result = self.api.search(tags)

            query = tags
            fetch_max_tweets = max_tweets/parsed_hashtags.__len__()
            # searched_tweets = [status for status in tweepy.Cursor(self.api.search, q=query, include_rts=False).items(max_tweets)]

            last_id = -1
            selected_count = 0
            while selected_count < fetch_max_tweets:
                logging.debug("Enter while loop. Selected counnt:- %s fetch_max_tweets:- %s", selected_count, fetch_max_tweets)
                count = fetch_max_tweets - selected_count
                try:
                    new_tweets = self.api.search(q=query, count=count, max_id=str(last_id - 1), result_type="mixed", lang="en")
                    if not new_tweets:
                        break

                    for tweet in new_tweets:
                        logging.debug("Enter for loop")
                        if not tweet.text.encode('utf-8').startswith('RT'):
                            logging.debug("Accept if condition for checking re tweets")
                            if tweet.entities.__contains__('media') and tweet.entities['media'][0]['type'] == 'photo':
                                logging.debug("Checking for photos in tweet")
                                continue
                            row = []
                            Search_Category = search_sentence
                            Tweeter_Hashtag = tags
                            Tweeter_Handle = tweet.user.screen_name.encode('utf-8')
                            Tweet_Message = tweet.text.encode('utf-8')
                            Tweet_Datetime = tweet.created_at
                            Tweet_Location = tweet.coordinates

                            Tweet_RetweetCount = tweet.retweet_count
                            Tweet_FavoriteCount = tweet.favorite_count
                            row.append(Search_Category)
                            row.append(Tweeter_Hashtag)
                            row.append(Tweeter_Handle)
                            row.append(Tweet_Message)
                            row.append(Tweet_Datetime)
                            row.append(Tweet_Location)
                            row.append(Tweet_RetweetCount)
                            row.append(Tweet_FavoriteCount)
                            table_data.append(row)
                            selected_count += 1

                    last_id = new_tweets[len(new_tweets)-1].id
                except tweepy.TweepError as e:
                    print e.message
                    logging.info("error message %s", e)
                    # depending on TweepError.code, one may want to retry or wait
                    #  to keep things simple, we will give up on an error

            print tags

        return table_data

