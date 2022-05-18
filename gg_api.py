import helpers.hosts
import helpers.awards
import helpers.winners_given_nominees
import helpers.presenters
import helpers.nominees
import helpers.bestdressed
import helpers.sentiment

import os.path
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
    print("Starting get_awards for year={}".format(year))
    return helpers.awards.get_awards(TWEETS[year]) 

def get_nominees(year):
    '''Nominees is a dictionary with the hard coded award
    names as keys, and each entry a list of strings. Do NOT change
    the name of this function or what it returns.'''
    print("Starting get_nominees for year={}".format(year))
    return helpers.nominees.get_nominees(year)

def get_winner(year):
    '''Winners is a dictionary with the hard coded award
    names as keys, and each entry containing a single string.
    Do NOT change the name of this function or what it returns.'''
    print("Starting get_winners for year={}".format(year))
    return helpers.winners_given_nominees.get_winner(year)

def get_presenters(year):
    '''Presenters is a dictionary with the hard coded award
    names as keys, and each entry a list of strings. Do NOT change the
    name of this function or what it returns.'''
    print("Starting get_presenters for year={}".format(year))
    return helpers.presenters.get_presenters(year)

##bonus requirements
def sentiment(year):
    print("[BONUS] Starting sentiment for year={}".format(year))
    return helpers.sentiment.get_sentiment(year)

def bestdressed(year):
    print("[BONUS] Starting best_dressed for year={}".format(year))
    return helpers.bestdressed.bestdressed(year)

def pre_ceremony():
    '''This function loads/fetches/processes any data your program
    will use, and stores that data in your DB or in a json, csv, or
    plain text file. It is the first thing the TA will run when grading.
    Do NOT change the name of this function or what it returns.'''

    ''' 
    get_tweets: pre-processes our tweets to make them more machine readable,
        also packages tweets into award-specific files (in /awardsandfilters/ sub-dir)
        to the best of its ability
    
    If testing pre-ceremony for full run time, delete all files in /awardsandfilters/
    EXCEPT for 'awardsandfilters.txt'. Also delete 'processedtweets2013.txt' and
    'processedtweets2015.txt'
    '''

    get_tweets(2013)
    get_tweets(2015)

    print("Pre-ceremony processing complete.")
    return

def main():
    '''This function calls your program. Typing "python gg_api.py"
    will run this function. Or, in the interpreter, import gg_api
    and then run gg_api.main(). This is the second thing the TA will
    run when grading. Do NOT change the name of this function or
    what it returns.'''

    '''
    **We expect `gg2013.json` and `gg2015.json` to exist in the main directory of this project when you run
    `pre_ceremony()` or `main()`**
    '''

    # Your code here
    def get_year():
        while True:
            year = input("Enter the year you'd like to examine: ")
            if os.path.exists("gg%s.json" %year):
                print("You've selected Golden Globes in the year {}! Gathering data now...\n".format(year))
                return year
            else:
                print("Not a valid year. Please try again")
    
    def format_name(name):
        return " ".join([x[0].upper() + x[1:] if len(x) > 1 else x.upper() for x in name.split(" ")])

    year = get_year()

    nominees = get_nominees(year)
    presenters = get_presenters(year)
    hosts = get_hosts(year)
    winners = get_winner(year)
    redcarpet = bestdressed(year)
    senti = sentiment(year)

    print('\n')
    result = "="*10 + "FOR {}".format(year) + "="*10 + "\n\n\n"

    # HOSTS
    result += "Hosts: " + ", ".join(hosts) + "\n"
    hostsenti = ', '.join(format_name(x[0]) for x in senti.get("hosts"))
    result += "Host Sentiment: " + hostsenti + "\n\n"

    # PRESENTERS, NOMINEES AND WINNERS
    awardoutputs = "===== PRESENTERS, NOMINEES, AND WINNERS (+ some sentiment analysis) =====\n\n"
    for i in range(len(OFFICIAL_AWARDS)):
        awardoutputs = awardoutputs + "=== " + OFFICIAL_AWARDS[i].upper() + " ===\n"

        presenter = "NONE FOUND 😔"
        if presenters.get(OFFICIAL_AWARDS[i]):
            presenter = format_name(presenters.get(OFFICIAL_AWARDS[i])[0])

        nomineelist = "NONE FOUND 😔"
        if nominees.get(OFFICIAL_AWARDS[i]):
            nomineelist = ', '.join(format_name(name) for name in nominees.get(OFFICIAL_AWARDS[i]))
            
        winner = "NOT FOUND 😔"
        if winners.get(OFFICIAL_AWARDS[i]):        
            winner = format_name(winners.get(OFFICIAL_AWARDS[i]))
        
        awardoutputs += "Presenter(s): " + presenter + "\n"
        awardoutputs += "Nominees: " + nomineelist + "\n"
        awardoutputs += "Winner: " + winner + "\n"

        if winner in senti.keys():
            winnersenti = senti.get(winner.lower())
            winnersentiment = ', '.join(x[0] for x in winnersenti)
            awardoutputs += "Sentiment around winner: " + winnersentiment + "\n"

        awardoutputs += "\n"
        result += awardoutputs

    result += "=== [BONUS] RED CARPET ===\n" + redcarpet + "\n"

    print(result)

    with open("results{}.txt".format(year), 'w') as f:
        f.write(result)
        print("Results are also written to results{}.txt!".format(year))

    return 


if __name__ == '__main__':
    pre_ceremony()
    main()
