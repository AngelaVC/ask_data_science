# Import Twitter credentials from credentials.py
from bot.credentials import consumer_key, consumer_secret
from bot.credentials import access_token, access_token_secret

# import tweepy to handle twitter interaction, import sleep to wait
import tweepy
from time import sleep

# import tweet generator
from tweet.generate import Generated

from random import randint
from time import sleep
from datetime import datetime

# Tweet a line every min minutes
# TODO include topic information
# TODO add a way to listen for mentions or replies

class tweetBot:
    ''' This class manages the regular tweeting
    Can enter a frequency in minutes. Default is 60. Should be sure it is >=2.
    '''

    def __init__(self, dbname='link_db.json', topic=None, frequency=60):
        self.dbname = dbname
        self.topic = topic
        self.frequency = frequency*60
        self.generator = None
        self.api = None
        self.lastTime = None
        self.lastTweet = None
        self.tweeting = False

    def setupBot(self):
        # Access and authorize twitter app and initialize api
        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_token_secret)
        self.api = tweepy.API(auth)

    def startTweeting(self):
        self.generator = Generated(self.dbname, self.topic)
        self.generator.getAll()
        self.tweeting = True
        while self.tweeting == True:
            self.postTweet()
            print("Posted tweet below at " + self.lastTime)
            print(self.lastTweet)
            lag = randint(self.frequency - int(self.frequency/2),
                          self.frequency + int(self.frequency/2))
            print("Time to next tweet: " + str(lag/60) + " min")
            sleep(lag)


    def postTweet(self):
        self.lastTweet = self.generator.writeTweet(self.topic)
        self.api.update_status(self.lastTweet)
        self.lastTime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
