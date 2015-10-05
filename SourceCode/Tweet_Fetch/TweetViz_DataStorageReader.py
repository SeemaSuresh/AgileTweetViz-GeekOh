'''
This file is the interface between TweetViz application and data. This knows where to move the data
whether to SQL or to File. Also from where to fetch data from file or SQL
Author: Harsha Kadekar
Date: 10/02/2015
Reference:
'''
from TweetViz_File_ReaderWriter import TweetVizFileReaderWriter
from TweetViz_File_ReaderWriter import TweetVizFileOperationException
from TweetViz_General import TweetVizSingleton
from TweetViz_General import TweetVizAESCipher

import mysql.connector
import ConfigParser


class TweetVizDataStorageReader(object):
    __metaclass__ = TweetVizSingleton

    def __init__(self):
        self._file_handler = None
        self._offline = False
        self._user_name = None
        self._password = None
        self._host = None
        self._database = None
        self._file_storage = None
        self._log_level = 0
        pass

    @property
    def offline(self):
        return self._offline

    @property.setter
    def offine(self, value):
        self._offline = value

    @property
    def file_handler(self):
        return self._file_handler

    def connect_to_db(self):
        connect = None
        try:
            connect = mysql.connector.connect(user=self._user_name, password=self._password, host=self._host, database=self._database)
        finally:
            if connect is not None:
                connect.close()
                connect = None
        return connect

    def disconnect_from_db(self, connect):
        if connect is not None:
            connect.close()
            connect = None
        pass


    def read_configuration_file(self):
        config = None
        return_value = 0
        cipher = None
        try:
            config = ConfigParser.ConfigParser()
            self._database = config.get('TweetVizDB', 'Database')
            self._user_name = config.get('TweetVizDB', 'User')
            cipher = TweetVizAESCipher()

            self._password = cipher.decrypt(config.get('TweetVizDB', 'Password'))
            self._host = config.get('TweetVizDB', 'Host')

            if config.get('TweetVizCommon', 'FileBased').lower() == 'true':
                self._offline = True

            self._file_storage = config.get('TweetVizCommon', 'FileMemory')

        finally:
            config = None
        return return_value

    # Search_Category\tTweeter_Handle\tTweet_Message\tTweet_DateTime\tTweet_Location\tNumber_Of_Retweets\tNumber_Of_Favorites\n
    def read_full_details_from_db(self):
        query = None
        connect = None
        cursor = None
        table_data = []
        try:
            connect = self.connect_to_db()
            if connect is None:
                # An error has occured log error
                connect = None
            else:
                cursor = connect.cursor()
                if cursor is None:
                    # An error has occured log error
                    cursor = None
                else:
                    query = ("SELECT SEARCH_CATEGORY, TWEETER_HANDLE, TWEET_MESSAGE, TWEET_DATETIME, TWEET_LOCATION, NUMBER_OF_TWEETS, NUMBER_OF_FAVORITES FROM TWEETVIZDB.TWEETS_TABLE")

                    cursor.execute(query)
                    row = []

                    for (search_category, tweeter_handle, tweet_message, tweet_datetime, tweet_location, no_of_retweets, no_of_favorites) in cursor:
                        row.append(search_category)
                        row.append(tweeter_handle)
                        row.append(tweet_message)
                        row.append(tweet_datetime)
                        row.append(tweet_location)
                        row.append(no_of_retweets)
                        row.append(no_of_favorites)
                        table_data.append(row)

                    cursor.close()
                    cursor = None
                    self.disconnect_from_db(connect)
                    connect = None
        finally:
            if cursor is not None:
                cursor.close()
                cursor = None
            if connect is not None:
                connect.close()
                connect = None
        return table_data

    def read_from_file(self):
        table_data = None
        file_handler = None
        try:
            file_handler = TweetVizFileReaderWriter(self._file_storage)
            table_data = file_handler.read_file()
        finally:
            file_hanlder = None
        return table_data

    def write_to_file(self, table_data):
        file_handler = None
        try:
            if table_data is not None and table_data.__len__() > 0:
                file_handler = TweetVizFileReaderWriter(self._file_storage, table_data)
                file_handler.write_file()
        finally:
            file_handler = None

    def insert_data_to_db(self, table_data):
        connect = None
        cursor = None
        return_value = 0
        try:
            connect = self.connect_to_db()
            cursor = connect.cursor()

            # search_category, tweeter_handle, tweet_message, tweet_datetime, tweet_location, no_of_retweets
            insert_tweet_query = ("INSERT INTO TWEETVIZ.TWEET_TABLE "
                            "(search_category, tweeter_handle, tweet_message, tweet_datetime, tweet_location, no_of_retweets, no_of_favorites) "
                            "VALUES (%s, %s, %s, %s, %s, %s, %s)")

            for row in table_data:
                search_category = row[0]
                tweeter_handle = row[1]
                tweet_message = row[2]
                tweet_datetime = row[3]
                tweet_location = row[4]
                no_of_retweets = row[5]
                no_of_favorites = row[6]

                insert_tweet_data = (search_category, tweeter_handle, tweet_message, tweet_datetime,tweet_location, no_of_retweets, no_of_favorites)

                cursor.execute(insert_tweet_query, insert_tweet_data)

            last_row_id = cursor.lastrowid

            cursor.close()
        finally:
            if cursor is not None:
                cursor.close()
                cursor = None
            if connect is not None:
                connect.close()
                connect = None

        return return_value

    def call_stored_procedure(self, table_data):
        connect = None
        cursor = None
        return_value = 0
        try:
            if table_data is None:
                # Error table_data cannot be None log it
                connect = None
            else:
                if table_data.__len__() <= 0:
                    # Error table_data is empty.
                    connect = None
                else:
                    connect = self.connect_to_db()
                    if connect is None:
                        # Error connection problem log it.
                        connect = None
                    else:
                        cursor = connect.cursor()

        finally:
            if cursor is not None:
                cursor.close()
                cursor = None
            if connect is not None:
                connect.close()
                connect = None
        return return_value
        pass

