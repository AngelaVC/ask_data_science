# ask_a_data_scientist

This code gathers blog posts from DataTau (and other sources in the future), collects the text, and uses that text to generate tweets that sound like they might have come from an absurd data scientists. You can use it to scrape any broad topic (e.g. job postings) to do something similar (e.g. absurd job posting tweets). This is currently in use at http://twitter.com/AskDataScience

# Dependencies
The scrapers need TinyDB, urllib, BeautifulSoup, and re. The bot needs tweepy as well as TinyDB, time, random, and datetime. The tweet generator needs re, tinydb, collections (for the Counter and defaultdict) and nltk.tokenize for the sentance tokenizer.

# scrape
The class scrape.web scrapes from websites (blogs and other sites), attempting to get rid of text contained in footers and other areas, so only useful text is collected. The class also records the title and url of the website. These websites are stored in a TinyDB.

# tweet
Right now, tweet.generate.Generated uses a simple generator to create sentences from trigrams. The trigrams are converted to the dictionary transitions, so that inputing a word, e.g. transitions['the'] will return a list of tuples that
come after the key, e.g. [('quick','brown'), ('best', 'burgers')]. The generator, adds the next word to a tweet, by randomly selecting a tuple from the list transitions[key]. Because all of the next pairs are in the list, this is actually implementing a Markov chain approach.

There is also a reader.readTweet that takes in new tweets and starts a reply. It does this in a simple way by either looking for bigrams that occur infrequently in the text collected in the TinyDB or (better) by looking for nouns that occur infrequently. The idea is that these would be a word or bigram that would be
possibly important in the tweet. It starts a response tweet with this word or words

# bot
The class bot.twitterbot.postTweet manages the interaction with the twitter bot. To use this part of the code, go to https://apps.twitter.com/ and get the credentials, placing them in this folder with the name credentials.py. There is also a replyListener that listens for a mention or reply to the bot and passes
any such tweets to tweet.reader

# tests
I am currently working through the implementation of unit tests, and these can all be found in this folder.

# What's next?
The following things are on my TODO list:
* Tweak the way that my generator selects the next word. Right now it selects two new words randomly based on
  current word trigram (but because repeats are in there it is operating Markovianly, if that's a word). But
  I have a couple of other ideas for how I might structure my selection. May need more text for this.
* Compose a better end to my tweets, my first idea is to run my trigrams in reverse and after threshold
  switch to looking for sentence enders.
* Implement code to focus on a topic.
* Improve my database of text, pulling in more websites and tweets.
* Improve the way my responder starts reply tweets, mining the tweet for the topic.
