'''
Developer Gowtham
Date 12 OCT 2015
reference - http://stackoverflow.com/questions/22469713/managing-tweepy-api-search
            https://nawarkhede.wordpress.com/2014/08/16/separating-tweets-from-text-image-videos-using-tweepy-python/
            http://www.benkhalifa.com/twitter-crawler-python
'''
import tweepy
import logging
import time
logging.basicConfig(filename='tweet.log', level=logging.INFO, format='%(asctime)s %(message)s')
from geopy import geocoders


class TweetFetcher:
    def __init__(self, consumer_key, consumer_secret):
        self.consumer_key = consumer_key
        self.consumer_secret = consumer_secret
        self.auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        self.api = tweepy.API(self.auth)
        self._No_Of_Tweets_to_fetch = 100
        self._type_of_tweets = "mixed"

    @property
    def No_Of_Tweets_Fetch(self):
        return self._No_Of_Tweets_to_fetch

    @No_Of_Tweets_Fetch.setter
    def No_Of_Tweets_Fetch(self, value):
        self._No_Of_Tweets_to_fetch = value

    @property
    def Type_Of_Tweets(self):
        return self._type_of_tweets

    @Type_Of_Tweets.setter
    def Type_Of_Tweets(self, value):
        self._type_of_tweets = value

    def get_tweets(self, parsed_hashtags, search_sentence):
        logging.debug("entered get_tweets")
        # hashtag_count = len(parsed_hashtags)
        # 'an implememtation to handle multiple hashtags'

        table_data = []
        logging.info("Table data %s", table_data)
        max_tweets = self.No_Of_Tweets_Fetch*parsed_hashtags.__len__()
        bException = False

        for tags in parsed_hashtags:
            logging.debug("Enter for loop")
            # return_result = self.api.search(tags)

            query = tags
            fetch_max_tweets = max_tweets/parsed_hashtags.__len__()
            # searched_tweets = [status for status in tweepy.Cursor(self.api.search, q=query, include_rts=False).items(max_tweets)]

            #if bException:
            #    break

            last_id = -1
            selected_count = 0
            while selected_count < fetch_max_tweets:
                logging.debug("Enter while loop. Selected counnt:- %s fetch_max_tweets:- %s", selected_count, fetch_max_tweets)
                count = fetch_max_tweets - selected_count
                if bException:
                    break
                try:
                    new_tweets = self.api.search(q=query, count=count, max_id=str(last_id - 1), result_type=self.Type_Of_Tweets, lang="en")
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
                            if Tweet_Message.__contains__('\xF0') or Tweet_Message.__contains__('\xF3'):
                                continue
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
                    logging.error("error message %s", e)
                    if e.reason == '[{u\'message\': u\'Rate limit exceeded\', u\'code\': 88}]':
                        time.sleep(900)
                    else:
                        # depending on TweepError.code, one may want to retry or wait
                        #  to keep things simple, we will give up on an error
                        bException = True

            print tags

        return table_data

