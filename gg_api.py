import helpers.hosts
import helpers.awards
import helpers.winners
import helpers.presenters
import helpers.nominees
import helpers.bestdressed
import helpers.sentiment

from nltk.sentiment import SentimentIntensityAnalyzer
import helpers.tweet_preprocessing as TP

OFFICIAL_AWARDS = ['cecil b. demille award', 'best motion picture - drama', 'best performance by an actress in a motion picture - drama', 'best performance by an actor in a motion picture - drama', 'best motion picture - comedy or musical', 'best performance by an actress in a motion picture - comedy or musical', 'best performance by an actor in a motion picture - comedy or musical', 'best animated feature film', 'best foreign language film', 'best performance by an actress in a supporting role in a motion picture', 'best performance by an actor in a supporting role in a motion picture', 'best director - motion picture', 'best screenplay - motion picture', 'best original score - motion picture', 'best original song - motion picture', 'best television series - drama', 'best performance by an actress in a television series - drama', 'best performance by an actor in a television series - drama', 'best television series - comedy or musical', 'best performance by an actress in a television series - comedy or musical', 'best performance by an actor in a television series - comedy or musical', 'best mini-series or motion picture made for television', 'best performance by an actress in a mini-series or motion picture made for television', 'best performance by an actor in a mini-series or motion picture made for television', 'best performance by an actress in a supporting role in a series, mini-series or motion picture made for television', 'best performance by an actor in a supporting role in a series, mini-series or motion picture made for television']

def get_tweets(year):
    return TP.get_tweets(year)

TWEETS = {'2013': get_tweets(2013), '2015': get_tweets(2015)}

def get_hosts(year):
    '''Hosts is a list of one or more strings. Do NOT change the name
    of this function or what it returns.'''
    print("Starting get_hosts for year={}".format(year))
    return helpers.hosts.get_hosts(TWEETS[year])

def get_awards(year):
    '''Awards is a list of strings. Do NOT change the name
    of this function or what it returns.'''
    # Your code here
    print("Starting get_awards for year={}".format(year))
    return helpers.awards.get_awards(TWEETS[year]) 

def get_nominees(year):
    '''Nominees is a dictionary with the hard coded award
    names as keys, and each entry a list of strings. Do NOT change
    the name of this function or what it returns.'''
    # Your code here
    print("Starting get_nominees for year={}".format(year))
    return helpers.nominees.get_nominees(year)

def get_winner(year):
    '''Winners is a dictionary with the hard coded award
    names as keys, and each entry containing a single string.
    Do NOT change the name of this function or what it returns.'''
    # Your code here
    print("Starting get_winners for year={}".format(year))
    return helpers.winners.get_winner(year)

def get_presenters(year):
    '''Presenters is a dictionary with the hard coded award
    names as keys, and each entry a list of strings. Do NOT change the
    name of this function or what it returns.'''
    # Your code here
    print("Starting get_presenters for year={}".format(year))
    return helpers.presenters.get_presenters(year)

def sentiment(year):
    return helpers.sentiment.get_sentiment(year)

def bestdressed(year):
    return helpers.bestdressed.bestdressed(year)

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
    pre_ceremony()
    main()
