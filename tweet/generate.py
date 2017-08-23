import re
from tinydb import TinyDB, Query
from collections import defaultdict
import random
from itertools import chain

enders = ['.', '!', '?', ';', ',', ':']

def clean_text(text):
    # cleans various text components
    text = re.sub("\u2019", "'", text)  # replace single quote with apostr
    text = re.sub(r"\b[0-9]+.\b", " ", text)  # numbers only
    text = re.sub(r"\b\w+@\w+.\w+\b", " ", text)  # email addresses
    text = " ".join(text.split())  # gets rid of multi spaces, \r etc

    return text


class Generated():
    ''' Class for generated tweet. Could include a topic, text, image, link.
    First just building the text part.
    Generated tweet based on text in db, which has 'text' field
    '''
    def __init__(self, db=None, topic=None):
        self.db = TinyDB(db)
        self.topic = topic
        self.text = None
        self.words = []
        self.trigrams = None
        self.transitions = None
        self.starters = None

    def getAll(self):
        self.gatherText()
        self.getWords()
        self.getTrigrams()
        self.getTransitions(enders)

    def debug(self):
        for item in self.db:
            print(item['text'])

    def gatherText(self):
        ''' Takes a TinyDB with a "text" field and combines all the text into
        a one list of texts
        '''
        all_text = ""
        for item in self.db:
            all_text = all_text + " " + clean_text(item['text'])
        self.text = all_text

    def getWords(self):
        self.words = re.findall(r"[\w']+|[.!?;,:]", self.text)

    def getTrigrams(self):
        '''Creates trigrams from words. If words has not yet been created
        executes getWords
        '''
        if len(self.words) == 0:
            self.getWords()

        self.trigrams = zip(self.words, self.words[1:], self.words[2:])

    def getTransitions(self, snt_end=enders):
        transitions = defaultdict(list)
        for one, two, three in self.trigrams:
            if (two not in snt_end) & (three not in snt_end):
                transitions[one].append([two, three])
        self.transitions = transitions

    def getRandomLink(self):
        links = []
        for item in self.db:
            links.extend(item['links'])
        return random.choice(links)

    def endTweet(self, start_word=None, tweet='', snt_end=enders):
        next_start = random.choice(self.transitions[start_word])
        tries = 0
        while len(set(next_start).intersection(set(snt_end))) == 0:
            next_start = random.choice(self.transitions[start_word])
            tries += 1
            if tries >= 25:
                return tweet + ' ' + self.getRandomLink()

        return tweet + next_start[0] + next_start[1], None, 0

    def firstWords(self, start_word=None, snt_end=enders):
        # Randomly select word after sentance ender
        # Start tweet with next word to tweet, return word after that
        if start_word is None:
            starters = []
            for ender in snt_end:
                starters.extend(self.transitions[ender])
            next_start = random.choice(starters)
            tweet = next_start[0].capitalize()
        else:
            tweet = start_word
            while len(self.transitions[start_word]) == 0:
                 start_word = random.choice(self.words)
            next_start = random.choice(self.transitions[start_word])
            tweet = tweet + ' ' + next_start[0]


        return tweet, next_start[1]

    def nextWords(self, tweet, current, snt_end=enders):
        # Randomly select word after current word
        # Add next word to tweet, return word after that
        if len(self.transitions[current]) > 0:
                next_start = random.choice(self.transitions[current])
            # if there are bi word choices after the current word, then
            # randomly choose another starting word
        else:
            while len(self.transitions[current]) == 0:
                current = random.choice(self.words)
            next_start = random.choice(self.transitions[current])

        tweet = tweet + ' ' + next_start[0]
        return tweet, next_start[1]


    def writeTweet(self, start_word=None, twt_num=1, num_tweets=1, snt_end=enders,
                      min_length=10):
        tweet, next_word = self.firstWords(start_word)
        while len(tweet)<110:
            tweet = tweet + ' ' + next_word
            tweet, next_word = self.nextWords(tweet, next_word)

        tweet = tweet + random.choice(['.','.','.','!','?',"?!?",'...'])
        return tweet

    # Old version of the tweet creation method
    # def writeTweet_v1(self, start_word=None, twt_num=1, snt_end=enders,
    #                   min_length=10):
    #     ''' This function starts with either a start word or a random choice
    #         of anything after a
    #         sentance ender. Tweet builds from there
    #         using trigrams. If tweet is too long, it is split into parts.
    #         If there is space, a link is enclosed.
    #     '''
    #
    #     # This allows us to continue tweets or start on a topic
    #     # by starting with given word if passed one in the function
    #     if start_word is not None:
    #         tweet = start_word
    #         if len(self.transitions[start_word]) > 0:
    #             next_start = random.choice(self.transitions[start_word])
    #             next_word = next_start[1]
    #         else:
    #             next_start = random.choice(self.transitions[
    #                                             random.choice(self.words)])
    #             next_word = next_start[1]
    #
    #     # if not passed a start word, first make sure to start on a capital ltr
    #     else:
    #         next_start = random.choice(random.choice(
    #                             [self.transitions[end] for end in snt_end]))
    #         tweet = next_start[0].capitalize()
    #         next_word = next_start[1]
    #
    #     # continue to build string until it gets close to tweet-length
    #     while (len(tweet) + len(next_word) < 90):
    #         if next_word in snt_end:
    #             if len(tweet) < 140-23:
    #                 tweet = tweet + self.getRandomLink()
    #             else:
    #                 tweet = tweet + random.choice(['.', '.', '!', '?'])
    #             return tweet, False, twt_num
    #
    #             # if len(tweet) > min_length:
    #             #     if len(tweet) < 140-23:
    #             #         tweet = tweet + self.getRandomLink()
    #             #     else:
    #             #         tweet = tweet + random.choice(['.', '.', '!', '?'])
    #             #     return tweet
    #             # else:
    #             #     tweet = tweet + random.choice(['.', '.', '!', '?'])
    #         else:
    #             tweet = tweet + ' ' + next_word
    #
    #         # this while loop makes sure that there are transitions from the
    #         # next_word, and if there are not,
    #         # randomly selectes a new next_word
    #         while self.transitions[next_word] == []:
    #             next_word = random.choice(self.words)
    #
    #         next_start = random.choice(self.transitions[next_word])
    #
    #         if next_start[0] in snt_end:
    #             return tweet + random.choice(
    #                                 ['.', '.', '!', '?']), False, twt_num
    #         else:
    #             tweet = tweet + ' ' + next_start[0]
    #             next_word = next_start[1]
    #
    #     tweet, next_word, twt_num = self.endTweet(next_word, tweet)


        # this places a hard cap on the number of continuations
        # if twt_num > 4:
        #     tweet = tweet + '!'
        #     next_word = None
        # else:
        #     tweet = tweet + " " + str(twt_num) + "/"
        # return tweet, next_word, twt_num
