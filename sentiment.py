from nltk.tokenize import wordpunct_tokenize
import json
import re
from collections import Counter
from textblob import TextBlob

def get_tweets(year):
    f = open("processedtweets{}.txt".format(year), 'r')
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
            'motion', 'picture', 's', 'm', 'w', 'papel', 't', 'en', 'best', 'i', 'mejor', 'el','é','o', 'n', "una","los","musical",
            "original","lleva","para", "un", "se","much","many",'u',"por","solvej","premio", "red", "f","h"]  #removing spanish stopwords as well
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
    winners = get_winners_answer(year)

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
                if winner == "daniel day-lewis":
                    winner = "daniel day lewis"
                elif winner == "j.k. simmons":
                    winner = "jk simmons"
                if winner not in winnersenti.keys():
                    winnersenti[winner] = Counter()
                name = winner.split()
                
                contains = all(n in tweet.lower() for n in name)

                if contains:
                    adj = getadj(name, tweet)
                    winnersenti[winner].update(adj)

    hostsenti["hosts"] = hostsenti["hosts"].most_common(4)
    for winner in winnersenti:
        winnersenti[winner] = winnersenti[winner].most_common(4)
    hostsenti.update(winnersenti)
    sentimentdictionary = hostsenti
    return sentimentdictionary
                				
# get_sentiment(2013)
# get_sentiment(2015)