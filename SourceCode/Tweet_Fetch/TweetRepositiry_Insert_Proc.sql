DELIMITER $$
CREATE DEFINER=`root`@`localhost` PROCEDURE `TweetRepository_Insert`(IN Hashtag varchar(767),
IN Tweet varchar(767), IN Location varchar(100), IN CreationTime datetime, IN RTCount INT, IN FavCount INT,
IN USerName Varchar(100))
BEGIN
Insert into tweet_repositoty (HashTag, Tweet, CreationTime, Location, RetweetCount, FavouriteCount, UserID ) 
values (Hashtag, Tweet, Location, CreationTime, RTCount, FavCount, UserName);

END$$
DELIMITER ;
