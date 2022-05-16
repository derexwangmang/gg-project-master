import json
import re
from os.path import exists
import unidecode

'''
PREPROCESSES TWEETS

JSON of Tweets => TXT file, line delimited of cleaned Tweet strings
Currently I've just been testing it and reading processed data into a .txt file through cmd line
As you can see in beginning of function, we can also store it in a .txt and read from it 
(as to not process tweets over and over again, processing takes a few seconds)
'''

HASHTAG_DIC = {}
MENTION_DIC = {}

def get_tweets(year):
    if exists('processedtweets{}.txt'.format(year)):
        return open('processedtweets{}.txt'.format(year)).readlines()


    with open('./gg{}.json'.format(year)) as f:
        tweet_information = json.load(f)

        tweet_text_lst = []

        for tweet in tweet_information:
            tweet = tweet['text']
            tweet = clean(tweet)
            tweet_text_lst.append(tweet)

    f = open('./processedtweets{}.txt'.format(year), 'w')
    for i, tweet in enumerate(tweet_text_lst):
        tweet_text_lst[i] = secondClean(tweet_text_lst[i])
        f.write(tweet_text_lst[i] + '\n')

    return tweet_text_lst

def secondClean(text):
    text = separateHashtags(text)
    text = fixMentions(text)
    # text = re.sub('(\'s\s*)', ' \1', text) 
    text = re.sub('([^a-zA-Z0-9\s\'])', ' ', text)
    text = re.sub('(\se\s)+', ' ', text)
    

    text = re.sub('\s+', ' ', text)
    if re.match('\s+', text):
        text = re.sub('\s+', '', text, 1)

    # text = re.sub('(?<=\((^|\s)[A-Z])\s+(?=([A-Z]($|\s)))*', '', text)
    # '(\s|^)[A-Z]\s[A-Z](\s|$)'
    return text

def clean(text):
    text = unidecode.unidecode(text)
    text = re.sub('&amp;', " and ", text)
    text = re.sub('(&gt;)+', ' are greater than ', text)
    text = re.sub('(&lt;3+)+', ' heartemote ', text)
    text = re.sub('(&lt;)+', " are less than ", text)
    text = re.sub(':\(+', ' frownemote ', text)
    text = re.sub(':\)+', ' smileemote ', text)
    text = re.sub('\s+', ' ', text)
    text = removeRT(text)
    text = removeLinks(text)
    text = separateHashtags(text)
    text = fixMentions(text)
    return text

def removeRT(text):
    rt = re.compile(r'RT @[a-zA-Z0-9_-]+(:?)\s')
    if re.search(rt, text) or re.match(rt, text):
        return re.sub(rt, "", text)
    return text

def removeLinks(text):
    link = re.compile('http(s?)\S*')
    if re.search(link, text):
        return re.sub(link, "", text)
    return text

def separateHashtags(text):
    hashtags = re.findall("#[a-zA-Z]*", text)
    for h in hashtags:
        if h.lower() in HASHTAG_DIC:
            text = re.sub(h, HASHTAG_DIC[h.lower()], text)
        elif h != h.lower():
            trans = re.sub(r'(?<!^)(?=[A-Z])', ' ', h)[1:]
            text = re.sub(h, trans, text)
            HASHTAG_DIC[h.lower()] = trans.lower()
    return text

def fixMentions(text):
    ats = re.findall("@[a-zA-Z0-9_]+", text)
    for a in ats:
        if a.lower() in MENTION_DIC:
            text = re.sub(a, MENTION_DIC[a.lower()], text)
        elif a != a.lower():
            trans = re.sub(r'(?<!^)(?=[A-Z])', ' ', a)[1:]
            trans = re.sub('\s*_\s*', ' ', trans)
            trans = re.sub('[0-9]*', '', trans)
            text = re.sub(a, trans, text)
            MENTION_DIC[a.lower()] = trans.lower()
    return text


#UNCOMMENT ME FOR TESTING "python3 tweet_preprocessing.py > tweets2013.txt"
get_tweets(2013)
