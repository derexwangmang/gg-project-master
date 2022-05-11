import json
import re
from collections import Counter
import helpers.awards

from nltk.corpus import stopwords as sw
from nltk.tokenize import wordpunct_tokenize
from nltk.sentiment import SentimentIntensityAnalyzer

OFFICIAL_AWARDS_1315 = ['cecil b. demille award', 'best motion picture - drama', 'best performance by an actress in a motion picture - drama', 'best performance by an actor in a motion picture - drama', 'best motion picture - comedy or musical', 'best performance by an actress in a motion picture - comedy or musical', 'best performance by an actor in a motion picture - comedy or musical', 'best animated feature film', 'best foreign language film', 'best performance by an actress in a supporting role in a motion picture', 'best performance by an actor in a supporting role in a motion picture', 'best director - motion picture', 'best screenplay - motion picture', 'best original score - motion picture', 'best original song - motion picture', 'best television series - drama', 'best performance by an actress in a television series - drama', 'best performance by an actor in a television series - drama', 'best television series - comedy or musical', 'best performance by an actress in a television series - comedy or musical', 'best performance by an actor in a television series - comedy or musical', 'best mini-series or motion picture made for television', 'best performance by an actress in a mini-series or motion picture made for television', 'best performance by an actor in a mini-series or motion picture made for television', 'best performance by an actress in a supporting role in a series, mini-series or motion picture made for television', 'best performance by an actor in a supporting role in a series, mini-series or motion picture made for television']
OFFICIAL_AWARDS_1819 = ['best motion picture - drama', 'best motion picture - musical or comedy', 'best performance by an actress in a motion picture - drama', 'best performance by an actor in a motion picture - drama', 'best performance by an actress in a motion picture - musical or comedy', 'best performance by an actor in a motion picture - musical or comedy', 'best performance by an actress in a supporting role in any motion picture', 'best performance by an actor in a supporting role in any motion picture', 'best director - motion picture', 'best screenplay - motion picture', 'best motion picture - animated', 'best motion picture - foreign language', 'best original score - motion picture', 'best original song - motion picture', 'best television series - drama', 'best television series - musical or comedy', 'best television limited series or motion picture made for television', 'best performance by an actress in a limited series or a motion picture made for television', 'best performance by an actor in a limited series or a motion picture made for television', 'best performance by an actress in a television series - drama', 'best performance by an actor in a television series - drama', 'best performance by an actress in a television series - musical or comedy', 'best performance by an actor in a television series - musical or comedy', 'best performance by an actress in a supporting role in a series, limited series or motion picture made for television', 'best performance by an actor in a supporting role in a series, limited series or motion picture made for television', 'cecil b. demille award']

stopwords = sw.words("english")

def tokenize(text):
    return [t.lower() for t in wordpunct_tokenize(text)]

def get_tweets(year):
    with open('gg{}.json'.format(year)) as f:
        tweet_information = json.load(f)

        tweet_text_lst = []
        for tweet in tweet_information:
            tweet_text_lst.append(tweet['text'])

    return tweet_text_lst

def get_hosts(year):
    '''Hosts is a list of one or more strings. Do NOT change the name
    of this function or what it returns.'''
    host_discussion_pattern = re.compile('hosted|hosting')
    host_relevant_tweets = list(filter(host_discussion_pattern.search, get_tweets(year)))

    host_multiple_names_pattern = re.compile('[A-Z][a-z]+ [A-Z][a-z]+ (and|&) [A-Z][a-z]+ [A-Z][a-z]+')
    host_mention_tweets = list(filter(host_multiple_names_pattern.search, host_relevant_tweets))

    host_name_pattern = re.compile('[A-Z][a-z]+ [A-Z][a-z]+')
    host_names = Counter()
    for tweet in host_mention_tweets:
        potential_names = host_name_pattern.findall(tweet)
        host_names.update(potential_names)
    hosts = []
    lstofhosts = host_names.most_common(2)
    for n,f in lstofhosts:
        hosts.append(n)
    return hosts

def get_awards(year):
    '''Awards is a list of strings. Do NOT change the name
    of this function or what it returns.'''
    # Your code here
    return helpers.awards.get_awards(year)

def get_nominees(year):
    '''Nominees is a dictionary with the hard coded award
    names as keys, and each entry a list of strings. Do NOT change
    the name of this function or what it returns.'''
    # Your code here
    return {}

def get_winner(year):
    '''Winners is a dictionary with the hard coded award
    names as keys, and each entry containing a single string.
    Do NOT change the name of this function or what it returns.'''
    # Your code here
    return {}

def get_presenters(year):
    '''Presenters is a dictionary with the hard coded award
    names as keys, and each entry a list of strings. Do NOT change the
    name of this function or what it returns.'''
    # Your code here
    return {}

def sentiment(year):
    sia = SentimentIntensityAnalyzer()
    siaps = sia.polarity_scores("Wow, NLTK is really powerful!")
    # print(siaps)

    def is_positive(tweet: str) -> bool:
        """True if tweet has positive compound sentiment, False otherwise."""
        return sia.polarity_scores(tweet)["compound"] > 0

    # for tweet in tweets:
    #     print(">", is_positive(tweet), tweet)
    return sentiment

def bestdressed(year):
    hashtag = "#redcarpet"
    return bestdressed

def pre_ceremony():
    '''This function loads/fetches/processes any data your program
    will use, and stores that data in your DB or in a json, csv, or
    plain text file. It is the first thing the TA will run when grading.
    Do NOT change the name of this function or what it returns.'''
    # Your code here
    print("Pre-ceremony processing complete.")
    return

def main():
    '''This function calls your program. Typing "python gg_api.py"
    will run this function. Or, in the interpreter, import gg_api
    and then run gg_api.main(). This is the second thing the TA will
    run when grading. Do NOT change the name of this function or
    what it returns.'''
    # Your code here
    return




if __name__ == '__main__':
    main()
