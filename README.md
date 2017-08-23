# ask_a_data_scientist

This work gathers blog posts from DataTau (and other sources in the future), collects the text, using them to generate tweets that sound like they might have come from an absurd data scientists.

# scrape
The class scrape.web scrapes from websites (blogs and other sites), attempting to get rid of text contained in footers and other areas, so only useful text is collected. The class also records the title and url of the website. These websites are stored in a TinyDB.

# tweet
Right now, tweet.generate.Generated uses a simple generator to create sentences from trigrams. The trigrams are converted to the dictionary transitions, so that inputing a word, e.g. transitions['the'] will return a list of tuples that
come after the key, e.g. [('quick','brown'), ('best', 'burgers')]. The generator, adds the next word to a tweet, by randomly selecting a tuple from the list transitions[key]. Future versions will retain a count and
implement a Markov chain approach.

# bot
The class bot.twitterbot.postTweet manages the interaction with the twitter bot. To use this part of the code, go to https://apps.twitter.com/ and get the credentials, placing them in this folder with the name credentials.py.

# tests
I am currently working through the implementation of unit tests, and these can all be found in this folder.

# What's next?
The following things are on my TODO list:
* Make my tweet generator more Markovian, keeping and using counts that help be to select best next words.  
  Right now it just does random selection out of all probabilities.
* Overlap the trigrams for better intelligibility (rewrite transitions to take in pairs of words as key).
  May need more text for this.
* Compose a better end to my tweets, my first idea is to run my trigrams in reverse and after threshold
  switch to looking for sentence enders.
* Implement code to start with a particular word.
* Implement code to focus on a topic.
* Improve my database of text, pulling in more websites and tweets.
* Write tweet responder to respond to mentions of @AskDataScience, including pulling word from mention tweet
