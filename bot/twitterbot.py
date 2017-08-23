# Import Twitter credentials from credentials.py
from credentials import consumer_key, consumer_secret
from credentials import access_token, access_token_secret

# import tweepy to handle twitter interaction, import sleep to wait
import tweepy
from time import sleep

# import tweet generator
import tweet.text

# Access and authorize twitter app and initialize api
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)


# Tweet a line every min minutes
# TODO include topic information
def postTweet(topic=None):
    generator = tweet.text.Generated('../link.db', topic)
    generator.getAll()
    new_tweet, next_word, num = generator.writeTweet()
    api.update_status(new_tweet)
    num = num + 1
    while next_word is not None:
        new_tweet, next_word, num = generator.writeTweet(next_word, num)
        api.update_status(new_tweet)
        num = num + 1
