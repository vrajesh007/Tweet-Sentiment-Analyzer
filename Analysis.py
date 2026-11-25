import os
import re
import tweepy
from better_profanity import profanity
from tweepy import OAuthHandler
from textblob import TextBlob


class TwitterClient(object):
    """Client for fetching tweets and classifying sentiment and profanity."""

    def __init__(self):
        consumer_key = os.environ.get("TWITTER_CONSUMER_KEY", "")
        consumer_secret = os.environ.get("TWITTER_CONSUMER_SECRET", "")
        access_token = os.environ.get("TWITTER_ACCESS_TOKEN", "")
        access_token_secret = os.environ.get("TWITTER_ACCESS_TOKEN_SECRET", "")

        self.api = None
        if not all([consumer_key, consumer_secret, access_token, access_token_secret]):
            print("Warning: Twitter API credentials are not configured in environment variables.")
            return

        try:
            self.auth = OAuthHandler(consumer_key, consumer_secret)
            self.auth.set_access_token(access_token, access_token_secret)
            self.api = tweepy.API(self.auth)
        except Exception as e:
            print(f"Error: Authentication failed ({e})")

    def clean_tweet(self, tweet):
        rex = re.sub(r"(@[A-Za-z0-9_]+)|([^0-9A-Za-z \t])|(\w+://\S+)", " ", tweet)
        return " ".join(rex.split())

    def get_tweet_sentiment(self, tweet):
        analysis = TextBlob(self.clean_tweet(tweet))
        if analysis.sentiment.polarity > 0:
            return "positive"
        elif analysis.sentiment.polarity == 0:
            return "neutral"
        else:
            return "negative"

    def get_tweets(self, query, count=100):
        if self.api is None:
            return []

        tweets = []
        try:
            fetched_tweets = self.api.search_tweets(q=query, count=count) if hasattr(self.api, "search_tweets") else self.api.search(q=query, count=count)
            for tweet in fetched_tweets:
                parsed_tweet = {
                    "text": tweet.text,
                    "sentiment": self.get_tweet_sentiment(tweet.text),
                    "profanity": profanity.contains_profanity(tweet.text),
                    "screen_name": tweet.user.screen_name,
                    "created_at": str(tweet.created_at),
                }
                if tweet.retweet_count > 0:
                    if parsed_tweet not in tweets:
                        tweets.append(parsed_tweet)
                else:
                    tweets.append(parsed_tweet)
            return tweets
        except Exception as e:
            print("Error : " + str(e))
            return []
