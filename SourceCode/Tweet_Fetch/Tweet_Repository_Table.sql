CREATE DATABASE if not exists TweetViz_DB


CREATE TABLE TweetViz_DB.tweet_repository (
  `Tweet_ID` int(11) NOT NULL AUTO_INCREMENT,
  `Search_Category` varchar(767) NOT NULL,
  `Tweeter_Hashtag` varchar(767) NOT NULL,
  `Tweeter_Handle` varchar(767) NOT NULL,
  `Tweet_Message` varchar(767) DEFAULT NULL,
  `Tweet_Datetime` datetime DEFAULT NULL,
  `Tweet_Location` varchar(100) DEFAULT NULL,
  `Tweet_RetweetCount` int(11) DEFAULT NULL,
  `Tweet_FavoriteCount` int(11) DEFAULT NULL,
  PRIMARY KEY (`Tweet_ID`,`Search_Category`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
