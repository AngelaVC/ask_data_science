from scrape import web
from urllib.request import urlopen
from tinydb import TinyDB, Query

import re

from collections import defaultdict

import random


def clean_text(text):
    text = re.sub("’","'",text)
    text = re.sub(r"’","'",text) # single quotes replace with apostrophe
    text = re.sub(r"\b[0-9]+.\b"," ",text)  #numbers only
    text = re.sub(r"\b\w+@\w+.\w+\b"," ",text) #email addresses
    text = " ".join(text.split()) # gets rid of multi spaces, \r etc

    return text


class Generated():
    ''' Class for generated tweet. Could include a topic, text, image, link.
    First just building the text part.
    '''
    def __init__(self, db):
        self.topic = None
        self.text = None
