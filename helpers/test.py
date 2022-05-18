import re
import nltk
from nltk import bigrams
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.util import everygrams
from nltk.corpus import stopwords
import Levenshtein

AWARD_STOP_WORDS = set(['by', 'an', 'in', 'a', 'performance', 'or', 'role', 'made', 'for', '-', ','])
TWEET_STOP_WORDS = set(["the", "golden", "globes", "for", "to", "and"])
STOPWORDS = set(stopwords.words('english'))

clean_award = ["cecil", "b", "demille", "award"]
def goodgram(gram):
    for g in gram:
        for sws in [award.split(' '), AWARD_STOP_WORDS, TWEET_STOP_WORDS, STOPWORDS]:
            for w in sws:
                if Levenshtein.ratio(g, w) >= 0.8:
                    return False
    return True

award = "cecil b. demille award"
year = 2013
with open('awardsandfilters/{}{}.txt'.format(re.sub("[^a-zA-Z]", "", award),year)) as f:
    all_tweets = f.readlines()

    people_names = {}
    other_names = {}
    for tweet in all_tweets:
        tweet = tweet.lower()
        sentences = sent_tokenize(tweet)
        for sentence in sentences:
            # print("NOW PARSING={}".format(sentence))
            # Start until key word

            bgrams = list(filter(goodgram, bigrams(word_tokenize(sentence))))
            for b in bgrams:
                if b in people_names:
                    people_names[b] += 1
                else:
                    people_names[b] = 1
            egrams = list(filter(goodgram, everygrams(word_tokenize(sentence), max_len=3)))

people_names = sorted(list(map(lambda x: [x, people_names[x]], people_names.keys())),\
    key=lambda y: -y[1])

print(people_names[:3])