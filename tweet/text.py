import re


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
        self.db = db
        self.topic = topic
        self.text = None
        self.words = []
        self.trigrams = None

    def gatherText(self):
        ''' Takes a TinyDB with a "text" field and combines all the text into
        a one list of texts
        '''
        all_text = ""
        for item in self.db:
            all_text + " " + clean_text(item['text'])
        self.text = all_text
        return self.text

    def getWords(self):
        self.words = re.findall(r"[\w']+|[.!?;,]", self.all_text)
        return self.words

    def getTrigrams(self):
        '''Creates trigrams from words. If words has not yet been created
        executes getWords
        '''
        if len(self.words) == 0:
            self.getWords()

        self.trigrams = zip(self.words, self.words[1:], self.words[2:])
        return self.trigrams
