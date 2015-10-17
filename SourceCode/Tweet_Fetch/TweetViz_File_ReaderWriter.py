'''
This file has all the code related to file IO operations. Like reading and writing tab delimited files
Author: Harsha Kadekar
Date: 10/02/2015
References: https://docs.python.org/2/tutorial/inputoutput.html -> For file Input/Output functions and classes
'''

# from TweetVizGeneral import TweetVizSingleton
import csv


class TweetVizFileOperationException(Exception):
    '''
    This is a custom exception used to handle file operations which is taking place in the TweetVizFileReaderWriter class
    '''

    def __init__(self, message, value):
        self.value = value
        self.message = message

    @property
    def value(self):
        return self.value

    @property
    def message(self):
        self.message

    def __str__(self):
        return "TWEETVIZ_ERROR:" + self.value.__str() + " :" + self.message


class TweetVizFileReaderWriter(object):
    '''
    This is a class which will handle all the file operations. It reads a csv files and gives a table containing that
    files content. Also if file name and table given, it can even write a tab separated file
    '''

    # __metaclass__ = TweetVizSingleton

    def __init__(self, file_name=None, tweet_table=None):
        self._file_name = file_name
        self._tweet_table = tweet_table
        pass

    @property
    def file_name(self):
        return self._file_name

    @file_name.setter
    def file_name(self, value):
        self._file_name = value

    @property
    def tweet_table(self):
        return self._tweet_table

    @tweet_table.setter
    def tweet_table(self, value):
        self._tweet_table = value

    def read_file(self):
        '''
        This function will read the file mentioned in _file_name of the class and once read it will fill the _tweet_table
        :return: This function is returning void
        '''
        tweet_table = []
        csv_file = None
        try:
            if self._file_name is not None:
                csv_file = open(self._file_name, 'rb')
                read = csv.reader(csv_file)
                # file_content = csv_file.read()
                # csv_file.close()
                # csv_file = None
                # line_no = 0
                # file_content = []
                for row in read:
                    tweet_table.append(row)

                self._tweet_table = tweet_table
                '''
                if file_content.__len__() > 0:
                    tweet_table = []
                    line_nos = 0
                    file_lines = file_content.split('n\r')
                    for line in file_lines:
                        row = []
                        if line_nos != 0:
                            columns = line.split('\t')
                            for column in columns:
                                row.append(column)
                            tweet_table.append(row)
                        line_nos += 1
                    self._tweet_table = tweet_table
                else:
                    self._tweet_table = tweet_table
                    raise TweetVizFileOperationException("File Content is empty:"+self._file_name, -4)
                '''
            else:
                self._tweet_table = tweet_table
                raise TweetVizFileOperationException("File name is not specified", -5)
        finally:
            if csv_file is not None:
                csv_file.close()
                csv_file = None

        return tweet_table

    def write_file(self):
        '''
        This function will write the contents of _tweet_table to the file mentioned in _file_name
        :return: This function is returning void
        '''
        csv_file = None
        try:
            if self._file_name is not None and self._tweet_table is not None:
                if self._tweet_table.__len__() > 0:
                    file_header = []
                    file_header.append('Search_Category')
                    file_header.append('Tweeter_Hashtag')
                    file_header.append('Tweeter_Handle')
                    file_header.append('Tweet_Message')
                    file_header.append('Tweet_Datetime')
                    file_header.append('Tweet_Location')
                    file_header.append('Tweet_RetweetCount')
                    file_header.append('Tweet_FavoriteCount')
                    # file_content = 'Search_Category\tTweeter_Hashtag\tTweet_Message\tTweeter_Handle\tTweet_Message\tTweet_Datetime\tTweet_Location\tTweet_RetweetCount\tTweet_FavoriteCount\n'
                    file_content = []
                    csv_file = open(self._file_name, 'wb')
                    wr = csv.writer(csv_file, quoting=csv.QUOTE_ALL)
                    wr.writerow(file_header)
                    for row in self._tweet_table:
                        wr.writerow(row)
                        '''
                        columns = ''
                        for column in row:
                            columns += column.__str__() + '\t'
                        file_content += columns + '\n\r'
                        '''

                    # csv_file = open(self._file_name, 'w')
                    # csv_file.write(file_content)
                    # csv_file.close()
                    # csv_file = None
                else:
                    raise TweetVizFileOperationException("Table Content is empty", -6)
            else:
                raise TweetVizFileOperationException("File name is not specified", -5)
        finally:
            if csv_file is not None:
                csv_file.close()
                csv_file = None
        pass
