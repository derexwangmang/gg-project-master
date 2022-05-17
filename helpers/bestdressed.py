import re
from collections import Counter
from textblob import TextBlob

def get_tweets(year):
    f = open("processedtweets{}.txt".format(year), 'r')
    tweets = f.readlines()
    return tweets

def bestdressed(year):
    redcarpet_pattern = re.compile('red carpet|redcarpet')
    redcarpet_tweets = list(filter(redcarpet_pattern.search, get_tweets(year)))
    name_pattern = re.compile('[A-Z][a-z]+ [A-Z][a-z]+')
    bestdressed = Counter()
    worstdressed = Counter()
    for tweet in redcarpet_tweets:
        name = name_pattern.findall(tweet)
        senti = TextBlob(tweet).sentiment[0]
        badwords = ["ugly", "horrible", "bad", "dislike", "hate", "gross", "worst", "fat","cakey","unflattering"]
        if senti > 0:
            bestdressed.update(name)
        elif any(word in tweet for word in badwords):
            worstdressed.update(name)
    del bestdressed['Golden Globes']
    del worstdressed['Golden Globes']

    for (key,value) in bestdressed.most_common(1):
        bestdressedperson = key
    for (key,value) in worstdressed.most_common(1):
        worstdressedperson = key

    result = bestdressedperson + " was the best dressed! " + worstdressedperson + " was the worst dressed!"
    return result

# bestdressed(2013)
# bestdressed(2015)