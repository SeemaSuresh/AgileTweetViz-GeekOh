SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='TRADITIONAL,ALLOW_INVALID_DATES';

CREATE SCHEMA IF NOT EXISTS `agiletweetviz` DEFAULT CHARACTER SET latin1 ;
USE `agiletweetviz` ;

-- -----------------------------------------------------
-- Table `agiletweetviz`.`tweet_repository`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `agiletweetviz`.`tweet_repository` (
  `Tweet_ID` INT(11) NOT NULL AUTO_INCREMENT,
  `HashTag` VARCHAR(767) NOT NULL,
  `Tweet` VARCHAR(767) NULL DEFAULT NULL,
  `CreationTime` DATETIME NULL DEFAULT NULL,
  `Location` VARCHAR(100) NULL DEFAULT NULL,
  `RetweetCount` INT(11) NULL DEFAULT NULL,
  `FavoriteCount` INT(11) NULL DEFAULT NULL,
  `UserID` VARCHAR(100) NULL DEFAULT NULL,
  PRIMARY KEY (`Tweet_ID`, `HashTag`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = latin1;

USE `agiletweetviz` ;

-- -----------------------------------------------------
-- procedure TweetRepository_Insert
-- -----------------------------------------------------

DELIMITER $$
USE `agiletweetviz`$$
CREATE DEFINER=`root`@`localhost` PROCEDURE `TweetRepository_Insert`(IN Hashtag varchar(767),
IN Tweet varchar(767), IN Location varchar(100), IN CreationTime datetime, IN RTCount INT, IN FavCount INT,
IN USerName Varchar(100))
BEGIN
Insert into tweet_repositoty (HashTag, Tweet, CreationTime, Location, RetweetCount, FavouriteCount, UserID ) 
values (Hashtag, Tweet, Location, CreationTime, RTCount, FavCount, UserName);

END$$

DELIMITER ;

SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
