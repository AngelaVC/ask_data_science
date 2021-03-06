# Import Twitter credentials from credentials.py
from bot.credentials import consumer_key, consumer_secret
from bot.credentials import access_token, access_token_secret

# import tweepy to handle twitter interaction, import sleep to wait
import tweepy

# import tweet generator
from tweet.generate import Generated
from tweet.reader import readTweet

# imports to handle sleeping between tweets
from time import sleep
from random import randint
from datetime import datetime

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

db = 'link_db.json'


# TODO need to fix the inheritance here so that I can pass the need to reply
# back to tweetBot so that I can use the tweetBot self.api

class replyListener(tweepy.StreamListener):
    def __init__(self, dbname, generator, api):
        self.db = dbname
        self.generator = generator
        self.api = api
        print(self.generator)

    def on_status(self, status):
        """Once status arrives, read, analyse, and start a response
        Then pass start to the generator function
        """
        print(status.text + " from " + status.user.screen_name)
        read_tweet = readTweet(self.db, status.text)
        read_tweet.getFreq()
        read_tweet.nounReplyStarter()
        self.generator.starter = read_tweet.replyStart
        reply = "@" + status.user.screen_name + ' ' \
                + self.generator.writeTweet()

        print('Try reply: ' + reply)
        # if reply is too long, start removing words from end
        while len(reply) > 140:
            reply_list = reply.split()
            reply_list = reply_list[:-1]
            reply = ' '.join(reply_list)
        print('Final reply: ' + reply)
        print('Reply length: ' + len(reply))

        # TODO want to pass tweetBot.api to the reply listener and
        # use that, but that is causing an error, so need to sort out
        api.update_status(reply, in_reply_to_status_id=status.id)
        print('Replied to ' + str(status.id))

    def on_error(self, status_code):
        print('Encountered error with status code:', status_code)
        return True  # Don't kill the stream

    def on_timeout(self):
        print('Timeout...')
        return True  # Don't kill the stream


class tweetBot:
    ''' This class manages the regular tweeting
        Can enter a frequency in minutes. Default is 60.
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
        ''' Access and authorize twitter app and initialize api
            Initialize generator to write tweets '''
        self.auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        self.auth.set_access_token(access_token, access_token_secret)
        self.api = tweepy.API(auth)
        self.generator = Generated(self.dbname, self.topic)
        self.generator.getAll()

    def startTweeting(self):
        ''' This sets self.tweeting to True
            and then calls postTweet at random intervals centered on
            user.frequency minutes '''
        if self.generator is None:
            self.setupBot()
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
        ''' Starts listening for mentions/replies to self.user
            using replyListener '''
        self.replying = True
        print("Listening for replies to " + self.user)
        listen = tweepy.streaming.Stream(self.auth, replyListener(self.dbname, self.generator, self.api))
        listen.filter(track=[self.user])
