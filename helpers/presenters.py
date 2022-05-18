import json
import re
from collections import Counter
from nltk.corpus import stopwords
from difflib import SequenceMatcher
from nltk.tokenize import word_tokenize, sent_tokenize
import Levenshtein


award_stop_words = set(['by', 'an', 'in', 'a', 'performance', 'or', 'role', 'made', 'for', '-', ',','is','best'])
nltk_stop_words = set(stopwords.words('english'))
nltk_stop_words.update(['http', 'golden', 'globes', 'goldenglobes', 'goldenglobe'])

OFFICIAL_AWARDS = ['cecil b. demille award', 'best motion picture - drama', 'best performance by an actress in a motion picture - drama', 'best performance by an actor in a motion picture - drama', 'best motion picture - comedy or musical', 'best performance by an actress in a motion picture - comedy or musical', 'best performance by an actor in a motion picture - comedy or musical', 'best animated feature film', 'best foreign language film', 'best performance by an actress in a supporting role in a motion picture', 'best performance by an actor in a supporting role in a motion picture', 'best director - motion picture', 'best screenplay - motion picture', 'best original score - motion picture', 'best original song - motion picture', 'best television series - drama', 'best performance by an actress in a television series - drama', 'best performance by an actor in a television series - drama', 'best television series - comedy or musical', 'best performance by an actress in a television series - comedy or musical', 'best performance by an actor in a television series - comedy or musical', 'best mini-series or motion picture made for television', 'best performance by an actress in a mini-series or motion picture made for television', 'best performance by an actor in a mini-series or motion picture made for television', 'best performance by an actress in a supporting role in a series, mini-series or motion picture made for television', 'best performance by an actor in a supporting role in a series, mini-series or motion picture made for television']

def get_tweets(year):
    with open('processedtweets{}.txt'.format(year)) as f:
        return f.readlines()

def get_presenters(year):
    awards = dict.fromkeys(OFFICIAL_AWARDS, None)
    award_mappings = get_filtered_awards(year)
    clean_awards = list(award_mappings.keys())

    for i, award in enumerate(OFFICIAL_AWARDS):
        awards[award] = get_presenters_by_award(year, award, clean_awards[i])

    return awards

def get_presenters_by_award(year, award, clean_award):
    output = Counter()
    presenter_pattern = re.compile('present')
    tweets = open("awardsandfilters/{}{}.txt".format(re.sub("[^a-zA-Z]", "", award), year)).readlines()
    tweets_containing_present = list(filter(presenter_pattern.search, tweets))
    for tweet in tweets_containing_present:
        pattern1 = re.search("([A-Z][a-z]*)[\s-]([A-Z][a-z]*)[\s-](and)[\s-]([A-Z][a-z]*)[\s-]([A-Z][a-z]*)", tweet)
        pattern2 = re.search("[A-Z]([a-z]+|\.)(?:\s+[A-Z]([a-z]+|\.))*(?:\s+[A-Z][a-z\-]+){0,1}\s+[A-Z]([a-z]+|\.)", tweet)
        pattern3 = re.search(r'\b(cecil)|(best)\s+([^.!?@:#-]*)', tweet, re.IGNORECASE)
        presenters = []
        if pattern1 and pattern3:
            name1 = pattern1.group(1) + ' ' + pattern1.group(2)
            name2 = pattern1.group(4) + ' ' + pattern1.group(5)
            presenters.append(name1)
            presenters.append(name2)
        elif pattern2 and pattern3:
            name1 = pattern2.group(0)
            check = [word for word in name1.split() if word.lower() in award_stop_words or word.lower() in nltk_stop_words]
            if not check:
                presenters.append(name1)
        for presenter in presenters:
            if presenter in output:
                output[presenter] += 1
            else:
                output[presenter] = 1
    res = []
    if output:
        targets = list(output.items())
        targets.sort(key = lambda tup: tup[1], reverse=True)
        count = 2
        while count > 0 and targets:
            potential = targets.pop(0)[0]
            if targets and Levenshtein.ratio(targets[0][0],potential) > .5:
                res.append(potential)
                targets.pop(0)
                continue
            else:
                res.append(potential)
                count -= 1
    return res

def get_filtered_awards(year):
    clean_awards = {}
    for award in OFFICIAL_AWARDS:
        text_lst = word_tokenize(award)
        filtered_text_lst = [token for token in text_lst if token not in award_stop_words]
        clean_awards[' '.join(filtered_text_lst)] = award
    return clean_awards
