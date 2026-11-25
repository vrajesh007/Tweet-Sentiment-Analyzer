import os
import re
import mysql.connector


def _get_db_config():
    return {
        "user": os.environ.get("MYSQL_USER", "root"),
        "password": os.environ.get("MYSQL_PASSWORD", "password"),
        "host": os.environ.get("MYSQL_HOST", "localhost"),
        "database": os.environ.get("MYSQL_DATABASE", "abusiveTweetsDB"),
        "port": int(os.environ.get("MYSQL_PORT", "3306")),
        "raise_on_warnings": True,
    }


class AbusiveTweetsDB:
    def writeToDB(self, profaneTweet):
        conn = mysql.connector.connect(**_get_db_config())
        c = conn.cursor()

        tweet = profaneTweet["text"]
        cleanTweet = re.sub(r"(@[A-Za-z0-9_]+)|([^0-9A-Za-z \t])|(\w+://\S+)", " ", tweet)
        sentiment = profaneTweet["sentiment"]
        abusive = str(profaneTweet["profanity"])
        screenName = profaneTweet["screen_name"]
        date = str(profaneTweet["created_at"])

        c.execute("SELECT * FROM abusiveTweetsTable")
        records = c.fetchall()
        flag = 0

        for record in records:
            if str(record[1]) == str(screenName):
                flag = 1
                if str(record[6]) != str(date):
                    temp = int(record[5]) + 1
                    sql = """UPDATE abusiveTweetsTable
                             SET Count = %s, Latest_Abusive_Tweet_by_User = %s, Sentiment = %s, Date = %s
                             WHERE SrNo = %s"""
                    c.execute(sql, (temp, cleanTweet, sentiment, date, record[0]))
                    break

        if flag == 0:
            sql = """INSERT INTO abusiveTweetsTable
                     (Name, Latest_Abusive_Tweet_by_User, Sentiment, Abusive, Count, Date)
                     VALUES (%s, %s, %s, %s, %s, %s)"""
            c.execute(sql, (screenName, cleanTweet, sentiment, abusive, 1, date))

        conn.commit()
        c.close()
        conn.close()

    def returnAllDataFromDatabase(self):
        conn = mysql.connector.connect(**_get_db_config())
        c = conn.cursor()
        c.execute("SELECT * FROM abusiveTweetsTable")
        records = c.fetchall()
        c.close()
        conn.close()
        return records
