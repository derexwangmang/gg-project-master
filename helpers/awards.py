import re
import nltk
from collections import Counter
from nltk import word_tokenize
from nltk.corpus import stopwords

STOPWORDS = stopwords.words('english')

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
            award_tokenized = word_tokenize(award)
            
            if award in potential_award_name:
                awards.pop(i)
                break
        
        awards.append(potential_award_name)

        if len(awards) >= 45:
            break
    
    cleaned_awards = clean_awards(awards)

    return cleaned_awards

def clean_awards(awards):
    tagged_awards = [nltk.pos_tag(word_tokenize(i)) for i in awards]
    cleaned_awards = []
    for i in range(len(tagged_awards)):
        if re.match('glo', tagged_awards[i][-1][0]):
            tagged_awards[i] = tagged_awards[i][:-2]
        elif re.match('gol', tagged_awards[i][-1][0]):
            tagged_awards[i] = tagged_awards[i][:-1]
        
        # cutting non-noun endings, but not 'musical' (it's a noun!)
        # also including 'wins' (it's a verb!s)
        while len(tagged_awards[i]) > 1 and ((tagged_awards[i][-1][1][0] != "N" and \
            not re.match('musical', tagged_awards[i][-1][0])) or \
                re.match('win', tagged_awards[i][-1][0])): 
                tagged_awards[i].pop(-1)
        
        if len(tagged_awards[i]) >= 2:
            award = " ".join(tagged_awards[i][j][0] for j in range(len(tagged_awards[i])))
            cleaned_awards.append(award)

    no_duplicate_awards = {}
    for a in cleaned_awards:
        a_nostops = [word for word in a.split(' ') if word not in STOPWORDS]
        a_nostops = " ".join(a_nostops)
        if a_nostops not in no_duplicate_awards:
            no_duplicate_awards[a_nostops] = a
        else:
            no_duplicate_awards[a_nostops] = max(a, no_duplicate_awards[a_nostops], key=lambda x: len(x))

    return list(no_duplicate_awards.values())