import re
from tinydb import TinyDB, Query
from collections import defaultdict
import random

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

    def writeTweet(self, snt_end=enders, min_length=10):
        ''' This function starts with a random choice anything after a
            sentance ender as the start of a tweet. Tweet builds from there
            using trigrams. If tweet is too long, it is split into parts.
            If there is space, a link is enclosed.
        '''
        next_start = random.choice(random.choice(
                                [self.transitions[end] for end in snt_end]))
        tweet = next_start[0]
        next_word = next_start[1]
        while (len(tweet) + len(next_word) < 135):
            if next_word in snt_end:
                if len(tweet) > min_length:
                    if len(tweet) < 140-23:
                        tweet = tweet + self.getRandomLink()
                    else:
                        tweet = tweet + random.choice(['.', '.', '!', '?'])
                    return tweet
                else:
                    tweet = tweet + random.choice(['.', '.', '!', '?'])
            else:
                tweet = tweet + ' ' + next_word

            if self.transitions[next_word] == []:
                next_start = random.choice(self.transitions[
                                                random.choice(self.words)])
            else:
                next_start = random.choice(self.transitions[next_word])

            if next_start[0] in snt_end:
                return tweet + random.choice(['.', '.', '!', '?'])
            else:
                tweet = tweet + ' ' + next_start[0]
                next_word = next_start[1]

        return tweet
