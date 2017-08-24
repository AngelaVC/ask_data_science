# Import Twitter credentials from credentials.py
from bot.credentials import consumer_key, consumer_secret
from bot.credentials import access_token, access_token_secret

# import tweepy to handle twitter interaction, import sleep to wait
import tweepy

# import tweet generator
from tweet.generate import Generated

# imports to handle sleeping between tweets
from time import sleep
from random import randint
from datetime import datetime

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)


# TODO need to fix the inheritance here so that I can pass the need to reply
# back to tweetBot
class replyListener(tweepy.StreamListener):
    def on_status(self, status):
        api.update_status("@" + status.user.screen_name +
                          " data science is awesome, but I don't know how to write smart answers yet. Soon!",
                          in_reply_to_status_id=status.id)
        print('Replied to ' + str(status.id))

    def on_error(self, status_code):
        print('Encountered error with status code:', status_code)
        return True  # Don't kill the stream

    def on_timeout(self):
        print('Timeout...')
        return True  # Don't kill the stream


class tweetBot:
    ''' This class manages the regular tweeting
    Can enter a frequency in minutes. Default is 60. Should be sure it is >=2.
    '''

    def __init__(self, user=None, dbname='link_db.json',
                 topic=None, frequency=60):
        self.user = user  # this should be screen name
        self.dbname = dbname
        self.topic = topic
        self.frequency = frequency*60
        self.generator = None
        self.auth = None
        self.api = None
        self.lastTime = None
        self.lastTweet = None
        self.tweeting = False
        self.replying = False

    def setupBot(self):
        ''' Access and authorize twitter app and initialize api'''
        self.auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        self.auth.set_access_token(access_token, access_token_secret)
        self.api = tweepy.API(auth)

    def startTweeting(self):
        ''' This initializes the generator, sets self.tweeting to True
            and then calls postTweet at random intervals '''
        self.generator = Generated(self.dbname, self.topic)
        self.generator.getAll()
        self.tweeting = True
        while self.tweeting is True:
            self.postTweet()
            print("Posted tweet below at " + self.lastTime)
            print(self.lastTweet)
            lag = randint(self.frequency - int(self.frequency/2),
                          self.frequency + int(self.frequency/2))
            print("Time to next tweet: " + str(lag/60) + " min")
            sleep(lag)

    def postTweet(self):
        ''' Creates tweet with writeTweet, uses self.api to post tweet,
            then records tweet as lastTweet and time as lastTime. Uses
            self.topic, not currently implemented in writeTweet. '''
        self.lastTweet = self.generator.writeTweet(self.topic)
        self.api.update_status(self.lastTweet)
        self.lastTime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    def startReplying(self):
        self.replying = True
        listen = tweepy.streaming.Stream(self.auth, replyListener())
        listen.filter(track=[self.user])
