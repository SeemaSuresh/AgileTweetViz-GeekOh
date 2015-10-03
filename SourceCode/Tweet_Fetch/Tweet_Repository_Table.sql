CREATE TABLE `tweet_repository` (
  `Tweet_ID` int(11) NOT NULL AUTO_INCREMENT,
  `HashTag` varchar(767) NOT NULL,
  `Tweet` varchar(767) DEFAULT NULL,
  `CreationTime` datetime DEFAULT NULL,
  `Location` varchar(100) DEFAULT NULL,
  `RetweetCount` int(11) DEFAULT NULL,
  `FavoriteCount` int(11) DEFAULT NULL,
  `UserID` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`Tweet_ID`,`HashTag`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
