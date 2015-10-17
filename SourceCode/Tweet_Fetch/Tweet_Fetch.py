'''
Developer Gowtham
Date 12 OCT 2015
reference - http://stackoverflow.com/questions/22469713/managing-tweepy-api-search
            https://nawarkhede.wordpress.com/2014/08/16/separating-tweets-from-text-image-videos-using-tweepy-python/
'''
import tweepy


class TweetFetcher:
    def __init__(self, consumer_key, consumer_secret):
        self.consumer_key = consumer_key
        self.consumer_secret = consumer_secret
        self.auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        self.api = tweepy.API(self.auth)

    def get_tweets(self, parsed_hashtags, search_sentence):
        # hashtag_count = len(parsed_hashtags)
        # 'an implememtation to handle multiple hashtags'

        table_data = []
        for tags in parsed_hashtags:
            # return_result = self.api.search(tags)

            query = tags
            max_tweets = 15
            # searched_tweets = [status for status in tweepy.Cursor(self.api.search, q=query, include_rts=False).items(max_tweets)]
            searched_tweets = []

            last_id = -1
            while len(searched_tweets) < max_tweets:
                count = max_tweets - len(searched_tweets)
                try:
                    new_tweets = self.api.search(q=query, count=count, max_id=str(last_id - 1), result_type="mixed")
                    if not new_tweets:
                        break

                    for tweet in new_tweets:
                        if not tweet.text.encode('utf-8').startswith('RT'):
                            if tweet.entities.__contains__('media') and tweet.entities['media'][0]['type'] == 'photo':
                                continue
                            row = []
                            Search_Category = search_sentence
                            Tweeter_Hashtag = tags
                            Tweeter_Handle = tweet.user.screen_name.encode('utf-8')
                            Tweet_Message = tweet.text.encode('utf-8')
                            Tweet_Datetime = tweet.created_at
                            Tweet_Location = tweet.geo
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

                    searched_tweets.extend(new_tweets)
                    last_id = new_tweets[-1].id
                except tweepy.TweepError as e:
                    print e.message
                    # depending on TweepError.code, one may want to retry or wait
                    #  to keep things simple, we will give up on an error
                break

            print tags
            # for tweets in return_result:
        return table_data

