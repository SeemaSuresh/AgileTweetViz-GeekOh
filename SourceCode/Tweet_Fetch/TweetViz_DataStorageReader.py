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
import logging
logging.basicConfig(filename='tweet.log', level=logging.INFO, format='%(asctime)s %(message)s')

class TweetVizDataStorageReader(object):
    '''
    This is the main class which is responsible for data storage and data loading from stored places.
    This is a singleton class
    '''
    __metaclass__ = TweetVizSingleton

    def __init__(self):
        self._user_name = None
        self._password = None
        self._host = None
        self._database = None
        self._file_storage = None
        self._log_level = 0
        pass

    def connect_to_db(self):
        logging.debug("Enter function connect_to_db")
        '''
        This function will connect to the database using the db crendentials. Once connected it will return the
        connector which can be used to do db operations.
        :return: Mysql connector
        '''
        connect = None
        # try:
        connect = mysql.connector.connect(user=self._user_name, password=self._password, host=self._host, database=self._database)
        '''
        finally:
            if connect is not None:
                connect.close()
                connect = None
        '''
        logging.debug("Leaving function connect_to_db with value of connect %s", connect)
        return connect

    def disconnect_from_db(self, connect):
        logging.debug("Enter function disconnect_from_db")
        '''
        This function will disconnect from the database.
        :param connect: Connector whose connection has to be closed
        :return: -
        '''
        if connect is not None:
            connect.close()
            connect = None

        logging.debug("Leave function disconnect_from_db")
        pass


    def read_configuration_file(self):
        logging.debug("Enter function read_configuration_file")
        '''
        This function will read the configuration file to get the configuraiton informations like DB connection info
        :return: -
        '''
        config = None
        return_value = 0
        cipher = None
        try:
            config = ConfigParser.ConfigParser()
            config.read("TweetViz_ConfigFile.ini")
            self._database = config.get('TweetVizDB', 'Database')
            self._user_name = config.get('TweetVizDB', 'User')
            cipher = TweetVizAESCipher('GeekOEncrypt1')
            # text = cipher.encrypt('Passionate79*')

            self._password = cipher.decrypt(config.get('TweetVizDB', 'Password'))
            self._host = config.get('TweetVizDB', 'Host')

            self._file_storage = config.get('TweetVizCommon', 'FileMemory')

        finally:
            config = None

        logging.debug("Leave function read_configuration_file with return_value:- %s", return_value)
        return return_value

    # Search_Category\tTweeter_Hashtag\tTweeter_Handle\tTweet_Message\tTweet_DateTime\tTweet_Location\tTweet_RetweetCount\tTweet_FavoriteCount\n
    def read_full_details_from_db(self):
        logging.debug("Enter function read_full_details_from_db")

        '''
        This function will read the tweets stored in sql table. Then forms a table and returns it.
        :return:Data present in the tweet_repository table.
        '''
        query = None
        connect = None
        cursor = None
        table_data = []
        table_header = []
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
                    query = ("SELECT Search_Category, Tweeter_Hashtag, Tweeter_Handle, Tweet_Message, Tweet_Datetime, Tweet_Location, Tweet_RetweetCount, Tweet_FavoriteCount FROM TweetViz_DB.tweet_repository")

                    cursor.execute(query)
                    row = []

                    table_header.append('Search_Category')
                    table_header.append('Tweeter_Hashtag')
                    table_header.append('Tweeter_Handler')
                    table_header.append('Tweet_Message')
                    table_header.append('Tweet_Datetime')
                    table_header.append('Tweet_Location')
                    table_header.append('Tweet_RetweetCount')
                    table_header.append('Tweet_FavoriteCount')

                    table_data.append(table_header)

                    for (Search_Category, Tweeter_Hashtag, Tweeter_Handle, Tweet_Message, Tweet_Datetime, Tweet_Location, Tweet_RetweetCount, Tweet_FavoriteCount) in cursor:
                        row.append(Search_Category)
                        row.append(Tweeter_Hashtag)
                        row.append(Tweeter_Handle)
                        row.append(Tweet_Message)
                        row.append(Tweet_Datetime)
                        row.append(Tweet_Location)
                        row.append(Tweet_RetweetCount)
                        row.append(Tweet_FavoriteCount)
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
                
        logging.debug("Leave function read_full_details_from_db with table:- %s", table_data)
        return table_data

    def read_from_file(self):
        logging.debug("Enter function read_from_file")

        '''
        This function will used the TweetVizFileReaderWriter class to read the tweets from a file.
        :return: table containing tweets. Table structure is same as sql tweet_reqpository table.
        '''
        table_data = None
        file_handler = None
        try:
            file_handler = TweetVizFileReaderWriter(self._file_storage)
            table_data = file_handler.read_file()
        finally:
            file_hanlder = None

        logging.debug("Leave function read_from_file with value of table data:- %s", table_data)
        return table_data

    def write_to_file(self, table_data):
        logging.debug("Enter function write_to_file")

        '''
        This function will be used to create a file containing tweet information. It uses
        TweetVizFileReaderWriter class to do this function.
        :param table_data: table structure is similar to sql tweet_repository table. It contains tweets information
        :return:
        '''
        file_handler = None
        try:
            if table_data is not None and table_data.__len__() > 0:
                file_handler = TweetVizFileReaderWriter(self._file_storage, table_data)
                file_handler.write_file()
        finally:
            file_handler = None

        logging.debug("Leave function write_to_file")
        pass

    def insert_data_to_db(self, table_data):
        logging.debug("Enter function insert_data_to_db")
        '''
        This function will write the tweets into the DB table tweet_repository.
        :param table_data: Table containing tweets information. Its structure is similar to tweet_repository table.
        :return:
        '''
        connect = None
        cursor = None
        return_value = 0
        try:
            connect = self.connect_to_db()
            cursor = connect.cursor()

            # search_category, tweeter_handle, tweet_message, tweet_datetime, tweet_location, no_of_retweets
            insert_tweet_query = ("INSERT INTO TweetViz_DB.tweet_repository "
                            "(Search_Category, Tweeter_Hashtag, Tweeter_Handle, Tweet_Message, Tweet_Datetime, Tweet_Location, Tweet_RetweetCount, Tweet_FavoriteCount) "
                            "VALUES (%s, %s, %s, %s, %s, %s, %s, %s)")

            for row in table_data:
                Search_Category = row[0]
                Tweeter_Hashtag = row[1]
                Tweeter_Handle = row[2]
                Tweet_Message = row[3]
                Tweet_Datetime = row[4]
                Tweet_Location = row[5]
                Tweet_RetweetCount = row[6]
                Tweet_FavoriteCount = row[7]

                insert_tweet_data = (Search_Category, Tweeter_Hashtag, Tweeter_Handle, Tweet_Message,Tweet_Datetime, Tweet_Location, Tweet_RetweetCount, Tweet_FavoriteCount)

                cursor.execute(insert_tweet_query, insert_tweet_data)

            last_row_id = cursor.lastrowid
            connect.commit()

            cursor.close()
            cursor = None

        finally:
            if cursor is not None:
                cursor.close()
                cursor = None
            if connect is not None:
                connect.close()
                connect = None

        logging.debug("Leave function insert_data_to_db with return value:- %s", return_value)
        return return_value

    def call_stored_procedure(self, table_data):
        logging.debug("Enter function call_stored_procedure")

        '''
        This function is currently not used. Calling of stored procedure is not known yet. Like calling a stored
        procedure with table as input. Rather we will be using above insert_data_to_db function to do the work.
        :param table_data: Tweet information to be stored in db.
        :return: success of failure.
        '''
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

        logging.debug("Leave function call_stored_procedure with return value:- %s", return_value)
        return return_value

