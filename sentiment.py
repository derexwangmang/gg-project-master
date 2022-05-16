# from nltk.corpus import stopwords as sw
from nltk.tokenize import wordpunct_tokenize
# from nltk.sentiment import SentimentIntensityAnalyzer
# from nltk.stem import WordNetLemmatizer as lemma
import json
import re
from collections import Counter
# from statistics import mean
from textblob import TextBlob
import pandas as pd
# import helpers.tweet_preprocessing as tp
# import spacy
# from spacy_langdetect import LanguageDetector
# from spacy.language import Language

def get_tweets(year):
    f = open("tweets2013.txt", 'r')
    tweets = f.readlines()
    return tweets

def get_answers(year):
    with open("gg{}answers.json".format(year),'rb') as f:
        answer_information = json.load(f)
    return answer_information

def get_host_answer(year):
    answer_info = get_answers(year)
    hostanswer = answer_info.get("hosts")
    return hostanswer

def get_winners_answer(year):
    answer_info = get_answers(year)
    winners = []
    award_data = answer_info.get("award_data")
    for award in award_data:
        info = award_data.get(award)
        winner = info.get("winner")
        #print(lst)
        winners.append(winner)
    return winners

def getadj(name, tweet):
    stopwords = ["golden", "globes", "globe", "goldenglobes", "goldenglobe", "@", 'in', 'an', 'a', 'actress', 'actor',
            'motion', 'picture', 's', 'm', 't', 'best', 'i', 'mejor', 'el','é','o', 'n', "una","los","musical",
            "original","lleva","para", "un", "se","much","many",'u',"por","solvej","premio"]  #removing spanish stopwords as well
    stopwords.extend(name)
    tokens = wordpunct_tokenize(tweet)
    newtweet = [token for token in tokens if token.lower() not in stopwords]
    cleantweet = " ".join(newtweet)
    blob = TextBlob(cleantweet)
    adj = [word.lower() for (word,tag) in blob.tags if tag == "JJ"]
    return adj

def get_sentiment(year):
    alltweets = get_tweets(year)
    hosts = get_host_answer(year)
    # nominees = get_nominees_answer(2013)
    # presenters = get_presenters_answer(2013)
    winners = get_winners_answer(2013)

    hostsenti = {"hosts": Counter()}
    winnersenti = {}

    for tweet in alltweets:
        
        tweet = re.sub(r'[^\w\s]', '', tweet)

        if hosts[0] in tweet.lower() or hosts[1] in tweet.lower():
            hostname1 = hosts[0].split()
            hostname2 = hosts[1].split()
            stopwords = ["golden", "globes", "globe", "goldenglobes", "goldenglobe", "@", 'in', 'an', 'a', 'actress', 'actor',
            'motion', 'picture', 's', 'm', 't', 'best', 'i', 'mejor', 'el','é','o', 'n', "una","los", "un", "se"]
            stopwords.extend([hostname1[0], hostname1[1], hostname2[0], hostname2[1]])
            tokens = wordpunct_tokenize(tweet)
            newtweet = [token for token in tokens if token.lower() not in stopwords]
            cleantweet = " ".join(newtweet)
            blob = TextBlob(cleantweet)
            adj = [word.lower() for (word,tag) in blob.tags if tag == "JJ"]
            hostsenti["hosts"].update(adj)
        else:
            for winner in winners:
                winner = winner.lower()
                if winner not in winnersenti.keys():
                    winnersenti[winner] = Counter()
                name = winner.split()
                
                if len(name) == 1 and name[0] in tweet.lower():
                    adj = getadj(name, tweet)
                    winnersenti[winner].update(adj)

                elif len(name) == 2 and (name[0].lower() in tweet.lower()) and (name[1].lower() in tweet.lower()):
                    adj = getadj(name, tweet)
                    winnersenti[winner].update(adj)

                elif len(name) == 3 and (name[0].lower() in tweet.lower()) and (name[1].lower() in tweet.lower()) and (name[2].lower() in tweet.lower()):
                    adj = getadj(name, tweet)
                    winnersenti[winner].update(adj)

    hostsenti["hosts"] = hostsenti["hosts"].most_common(4)
    for winner in winnersenti:
        winnersenti[winner] = winnersenti[winner].most_common(4)
    hostsenti.update(winnersenti)
    sentimentdictionary = hostsenti
    return sentimentdictionary
                				
# get_sentiment(2013)
print(get_sentiment(2015))

# def detectlang(text):
#     @Language.factory("language_detector")
#     def get_lang_detector(nlp, name):
#         return LanguageDetector()
#     nlp = spacy.load("en_core_web_sm")
#     nlp.add_pipe('language_detector', last=True)
#     detect_language = nlp(text)._.language
#     lang = detect_language.get('language')
#     return lang
