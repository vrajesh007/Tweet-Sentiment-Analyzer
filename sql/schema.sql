CREATE DATABASE IF NOT EXISTS abusiveTweetsDB;
USE abusiveTweetsDB;

CREATE TABLE IF NOT EXISTS abusiveTweetsTable (
    SrNo INT NOT NULL AUTO_INCREMENT,
    Name VARCHAR(255) NOT NULL,
    Latest_Abusive_Tweet_by_User VARCHAR(280) NOT NULL,
    Sentiment VARCHAR(16) NOT NULL,
    Abusive VARCHAR(8) NOT NULL,
    Count INT DEFAULT 0,
    Date VARCHAR(64) NOT NULL,
    PRIMARY KEY (SrNo)
);
