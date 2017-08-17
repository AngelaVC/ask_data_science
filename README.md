# ask_a_data_scientist

This work gathers blog posts from DataTau (and possibly other sources in the future) for the purpose of collecting text that can be used for generating tweets that sound data-sciency.

# Scrape
The class scrape.web scrapes from websites (blogs and other sites), attempting to get rid of text contained in footers and other areas, so only useful text is collected. The class also records the title and url of the website. These websites are stored in a TinyDB.

# Tweet
Right now, this uses a simple generator to create sentances from trigrams.

