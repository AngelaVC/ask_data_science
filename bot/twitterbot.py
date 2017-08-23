# Import Twitter credentials from credentials.py
from credentials import consumer_key, consumer_secret
from credentials import access_token, access_token_secret

# import tweepy to handle twitter interaction, import sleep to wait
import tweepy
from time import sleep

# import tweet generator
import tweet.text

from random import randint
from time import sleep
from datetime import datetime

# Tweet a line every min minutes
# TODO include topic information
# TODO add a way to listen for mentions or replies

class tweetBot():
    ''' This class manages the regular tweeting
    Can enter a frequency in minutes. Default is 60. Should be sure it is >=2.
    '''

    def __init__(self):
        self.lastTime = None
        self.lastTweet = None
        self.tweeting = False

    def startTweeting(self, frequency=60):
        # Access and authorize twitter app and initialize api
        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_token_secret)
        api = tweepy.API(auth)

        generator = tweet.text.Generated('../link.db', topic)
        generator.getAll()

        self.tweeting = True
        while self.tweeting == True:
            self.lastTweet = self.postTweet()
            self.lastTime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            sleep(randint(frequency - int(frequency/2),frequency + int(frequency/2)))


    def postTweet(topic=None):
        api.update_status(generator.writeTweet())
