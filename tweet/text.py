import re
from tinydb import TinyDB, Query
from collections import defaultdict
import random


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
        self.getTransitions()

    def gatherText(self):
        ''' Takes a TinyDB with a "text" field and combines all the text into
        a one list of texts
        '''
        all_text = ""
        for item in self.db:
            all_text + " " + clean_text(item['text'])
        self.text = all_text

    def getWords(self):
        self.words = re.findall(r"[\w']+|[.!?;,]", self.text)

    def getTrigrams(self):
        '''Creates trigrams from words. If words has not yet been created
        executes getWords
        '''
        if len(self.words) == 0:
            self.getWords()

        self.trigrams = zip(self.words, self.words[1:], self.words[2:])

    def getTransitions(self):
        transitions = defaultdict(list)
        for one, two, three in self.trigrams:
            transitions[one].append([two, three])
        self.transitions = transitions

    def writeTweet(self):
        print(self.transitions)
        snt_end = ['.', '!', '?', ';']
        next_start = random.choice(self.transitions['.'])
        sentance = next_start[0]
        next_word = next_start[1]
        while (next_word not in snt_end) & (next_word is not None):
            sentance = sentance + ' ' + next_word
            next_start = random.choice(self.transitions[next_word])
            if next_start[0] in snt_end:
                return sentance + ' ' + next_start[0]
            else:
                sentance = sentance + ' ' + next_start[0]
                next_word = next_start[1]

        return sentance
