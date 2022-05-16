import json
from collections import Counter
from re import A
from nltk import bigrams
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.util import everygrams
import Levenshtein

AWARD_STOP_WORDS = set(['by', 'an', 'in', 'a', 'performance', 'or', 'role', 'made', 'for', '-', ','])
TWEET_STOP_WORDS = set(["the", "golden", "globes", "for", "to", "and"])

OFFICIAL_AWARDS = ['cecil b. demille award', 'best motion picture - drama', 'best performance by an actress in a motion picture - drama', 'best performance by an actor in a motion picture - drama', 'best motion picture - comedy or musical', 'best performance by an actress in a motion picture - comedy or musical', 'best performance by an actor in a motion picture - comedy or musical', 'best animated feature film', 'best foreign language film', 'best performance by an actress in a supporting role in a motion picture', 'best performance by an actor in a supporting role in a motion picture', 'best director - motion picture', 'best screenplay - motion picture', 'best original score - motion picture', 'best original song - motion picture', 'best television series - drama', 'best performance by an actress in a television series - drama', 'best performance by an actor in a television series - drama', 'best television series - comedy or musical', 'best performance by an actress in a television series - comedy or musical', 'best performance by an actor in a television series - comedy or musical', 'best mini-series or motion picture made for television', 'best performance by an actress in a mini-series or motion picture made for television', 'best performance by an actor in a mini-series or motion picture made for television', 'best performance by an actress in a supporting role in a series, mini-series or motion picture made for television', 'best performance by an actor in a supporting role in a series, mini-series or motion picture made for television']

# Returns all tweet text from year in lowercase without stop words
def get_tweets(year):
    tweet_text_lst = []
    with open('gg{}.json'.format(year), encoding='utf-8') as f:
        tweet_information = json.load(f)
        for tweet in tweet_information:
            text_lst = word_tokenize(tweet["text"])
            if text_lst[0].lower() == "rt":
                # For "RT @Forever21: Oh, Adele", removes RT, @, Forever21, :
                text_lst = text_lst[4:]

            english_text_lst = [token for token in text_lst if token.isalpha() and token.lower() not in TWEET_STOP_WORDS]
            tweet_text_lst.append(' '.join(english_text_lst))
    
    return tweet_text_lst

# Returns dictionary mapping between KEY = clean name, VALUE = original name
def get_filtered_awards(year):
    clean_awards = {}
    for award in OFFICIAL_AWARDS:
        text_lst = word_tokenize(award)
        filtered_text_lst = [token for token in text_lst if token not in AWARD_STOP_WORDS]
        clean_awards[' '.join(filtered_text_lst)] = award
        # clean_awards[frozenset(filtered_text_lst)] = award

    return clean_awards

def get_nominees(year):
    award_mappings = get_filtered_awards(year)
    clean_awards = award_mappings.keys()
    
    potential_nominees = {}
    for clean_award in clean_awards:
        potential_nominees[clean_award] = Counter()

    all_tweets = get_tweets(year)
    # all_tweets = ["John Doe is nominated for the cecil b. demille award.", "Argo was nominated for the best motion picture in drama. Jennifer Lawrence was nominated for the best actress performance in a motion picture drama."]
    # all_tweets = ["John Doe is nominated for the cecil b. demille award.", "John Doe was nominated for the cecil b. demille award.", "Johnny Doe is nominated for the cecil b. demille award."]
    for tweet in all_tweets:
        sentences = sent_tokenize(tweet)
        people_names = []
        other_names = []
        nominee_strings = [" is nominated for ", " was nominated for ", " nominated ", " nominees ", " should won ", " should been "]
        for sentence in sentences:
            # print("NOW PARSING={}".format(sentence))
            # Start until key word
            for nominee in nominee_strings:
                nominee_index = sentence.find(nominee)
                if nominee_index != -1:
                    # print("Found nominee!")
                    tokens = word_tokenize(sentence[:nominee_index])
                    people_names.append([sentence[nominee_index + len(nominee):], list(bigrams(tokens))])
                    other_names.append([sentence[nominee_index + len(nominee):], list(everygrams(tokens, max_len=3))])
            
            # print("PEOPLE NAMES: ", people_names)
            # print("OTHER NAMES: ", other_names)
            
            # Start after key word

        for award in clean_awards:
            # People award, needs two names
            if any(word in award for word in ["actor", "actress", "director", "demille"]):
                for potential_award, people_name in people_names:
                    filtered_potential_award = ' '.join([token for token in word_tokenize(potential_award) if token not in AWARD_STOP_WORDS])
                    # print("AWARD={}, POTENTIAL_AWARD={}, RATIO={}, PEOPlE_NAME={}".format(award, filtered_potential_award, Levenshtein.ratio(award, filtered_potential_award), people_name))
                    if Levenshtein.ratio(award, filtered_potential_award) >= 0.6:
                        for gram in people_name:
                            phrase = ' '.join(gram)
                            phrase = phrase.lower()
                            potential_nominees[award][phrase] = potential_nominees[award].get(phrase, 0) + 1
            else:
                for potential_award, other_name in other_names:
                    filtered_potential_award = ' '.join([token for token in word_tokenize(potential_award) if token not in AWARD_STOP_WORDS])
                    # print("AWARD={}, POTENTIAL_AWARD={}, RATIO={}".format(award, filtered_potential_award, Levenshtein.ratio(award, filtered_potential_award)))
                    if Levenshtein.ratio(award, filtered_potential_award) >= 0.6:
                        for gram in other_name:
                            phrase = ' '.join(gram)
                            phrase = phrase.lower()
                            potential_nominees[award][phrase] = potential_nominees[award].get(phrase, 0) + 1
    
    collapsed_potential_nominees = {}
    for clean_award in clean_awards:
        collapsed_potential_nominees[clean_award] = Counter()
    
    for award in clean_awards:
        for potential_winner in potential_nominees[award].keys():
            # print("Potential winner: ", potential_winner)
            added = False
            
            for collapsed_potential_winner in collapsed_potential_nominees[award].keys():
                # print("POTENTIAL WINNER={}, COLLAPSED={}".format(potential_winner, collapsed_potential_winner))
                # print("CURRENT FREQ COUNT: ", collapsed_potential_nominees[award][potential_winner])
                if Levenshtein.ratio(collapsed_potential_winner, potential_winner) >= 0.8:
                    # print("Ratio > 0.6")
                    collapsed_potential_nominees[award][collapsed_potential_winner] += 1
                    added = True
            
            if not added:
                collapsed_potential_nominees[award][potential_winner] = potential_nominees[award][potential_winner]
                # print("Added: ", collapsed_potential_nominees[award])
    
    print(collapsed_potential_nominees)
    nominees = {}
    for award in clean_awards:
        award_name = award_mappings[award]
        # print("AWARD NAME={}".format(award_name))
        if len(collapsed_potential_nominees[award]) > 0:
            nominees[award_name] = []
            for nominee in collapsed_potential_nominees[award].most_common(5):
                nominees[award_name].append(nominee[0])
        else:
            nominees[award_name] = ["Not found"]

        # print("\n")

    print(nominees)
    return nominees


# get_nominees('2013')