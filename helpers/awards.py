import re
import nltk
from collections import Counter

# Gets the awards for a given year
def get_awards(tweets):
    tweets = [tweet.lower() for tweet in tweets]
    # Scanning forward words
    won_pattern = re.compile('got|won|wins|is awarded')
    tweets_containing_won = list(filter(won_pattern.search, tweets))

    best_pattern = re.compile(r'\bbest\s+([^.!?@]*)')
    tweets_containing_best = list(filter(best_pattern.search, tweets_containing_won))
    award_tweets = []
    for tweet in tweets_containing_best:
        if best_pattern.search(tweet):
            match = best_pattern.search(tweet)
            tokenized_match = nltk.tokenize.word_tokenize(match.group(0))
            
            added_word = False
            for i, token in enumerate(tokenized_match):
                if token in ["for", "at", "on", "#"] or nltk.pos_tag([token])[0][1] in ["VB", "VBG", "VBD", "VBN", "VBP", "VBZ"]:
                    award_tweets.append(' '.join(tokenized_match[:i]))
                    added_word = True
                    break
            
            if not added_word:
                award_tweets.append(match.group(0))

    award_names_dict = Counter()
    for tweet in award_tweets:
        splitted_word = tweet.split()
        for i in range(len(splitted_word)):
            temp = ' '.join(splitted_word[:i+1])
            award_names_dict[temp] = award_names_dict.get(temp, 0) + 1

    # Scanning backwards
    won_pattern = re.compile('goes to|receive[sd]')
    tweets_containing_won = list(filter(won_pattern.search, tweets))

    best_pattern = re.compile(r'\bbest\s+.*([goes to|receive[sd]]*)')
    tweets_containing_best = list(filter(best_pattern.search, tweets_containing_won))
    award_tweets = []
    for tweet in tweets_containing_best:
        if best_pattern.search(tweet):
            match = best_pattern.search(tweet)
            tokenized_match = nltk.tokenize.word_tokenize(match.group(0))
            
            added_word = False
            for i, token in enumerate(tokenized_match):
                if token in ["goes", "receive"]:
                    award_tweets.append(' '.join(tokenized_match[:i]))
                    added_word = True
                    break
            
            if not added_word:
                award_tweets.append(match.group(0))

    # award_names_dict = Counter()
    for tweet in award_tweets:
        splitted_word = tweet.split()
        for i in range(len(splitted_word)):
            temp = ' '.join(splitted_word[:i+1])
            award_names_dict[temp] = award_names_dict.get(temp, 0) + 1

    awards = []
    for potential_award_name, _ in award_names_dict.most_common():
        if potential_award_name == "best":
            continue

        if potential_award_name[-1] in [",", "-"]:
            continue

        for i, award in enumerate(awards):
            if award in potential_award_name:
                awards.pop(i)
                break
        
        awards.append(potential_award_name)

        if len(awards) == 40:
            break
    
    return awards