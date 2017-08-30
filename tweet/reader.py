import re
from collections import defaultdict
from tweet.generate import Generated
import nltk
import random


def is_noun(word):
    POS = nltk.pos_tag([word])[0][1]
    return POS.startswith('NN')


class readTweet():
    def __init__(self, db=None, tweet=None):
        self.generator = Generated(db)
        self.tweet = tweet
        self.topic = None
        self.words = re.findall(r"[\w']+|[.!?;,:]", self.tweet)
        self.nouns = []
        self.nounFreq = defaultdict(list)
        self.wordFreq = defaultdict(list)
        self.bigrams = zip(self.words, self.words[1:])
        self.bigramFreq = defaultdict(list)
        self.replyStart = ''

    def getFreq(self):
        for word in self.words:
            self.wordFreq[word] = self.generator.wordFreq[word]

        for bigram in self.bigrams:
            self.bigramFreq[bigram] = self.generator.bigramFreq[bigram]

        self.getNouns()

    def getNouns(self):
        self.nouns = [word for word in self.words if is_noun(word)]

        for noun in self.nouns:
            self.nounFreq[noun] = self.generator.wordFreq[noun]

    def bigramReplyStarter(self):
        # This takes the bigram that occurs least frequently in all of the
        # text bigram and uses it to start a tweet
        # TODO need to take out any sentance enders (so that they don't appear
        # in tweet starter
        best_count = 1000000
        for key in self.bigramFreq:
            if (self.bigramFreq[key] > 0) & (self.big.ramFreq[key] < best_count):
                self.replyStart = key[0] + ' ' + key[1]
                best_count = self.bigramFreq[key]
        if best_count == 1000000:
            self.replyStart = "What are you talking about?"

    def nounReplyStarter(self):
        # This takes the least frequent noun and uses it to start a reply
        best_count = 1000000
        for key in self.nounFreq:
            if (self.nounFreq[key] > 0) & (self.nounFreq[key] < best_count):
                next_start = random.choice(self.generator.transitions[key])
                # need to reselect if next_start contains a sentance ender
                # will escape after 25 tries
                try_count = 0
                while (len(set(next_start).intersection(
                       set(self.generator.enders))) > 0) & try_count < 25:
                    next_start = random.choice(self.generator.transitions[key])
                    try_count += 1

                # update replyStart and the best_count before going to next
                self.replyStart = key.capitalize() + ' ' + ' '.join(next_start)
                best_count = self.nounFreq[key]

        if best_count == 1000000:
            # this happens if none of the keys
            self.replyStart = "What are you talking about? "
