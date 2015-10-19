/* Name: TweetViz_DB 
    Author: Seema Suresh */
CREATE DATABASE if not exists TweetViz_DB DEFAULT CHARACTER SET utf8mb4 DEFAULT COLLATE utf8mb4_general_ci


CREATE TABLE TweetViz_DB.tweet_repository (
  `Tweet_ID` int(11) NOT NULL AUTO_INCREMENT,
  `Search_Category` nvarchar(255) NOT NULL,
  `Tweeter_Hashtag` nvarchar(767) NOT NULL,
  `Tweeter_Handle` nvarchar(767) NOT NULL,
  `Tweet_Message` nvarchar(767) DEFAULT NULL,
  `Tweet_Datetime` datetime DEFAULT NULL,
  `Tweet_Location` nvarchar(100) DEFAULT NULL,
  `Tweet_RetweetCount` int(11) DEFAULT NULL,
  `Tweet_FavoriteCount` int(11) DEFAULT NULL,
  PRIMARY KEY (`Tweet_ID`,`Search_Category`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
