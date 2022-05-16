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

# Get all possible candidates for award
# Includes both nominees and winner
def get_candidates(year):
    candidates = {}
    with open('gg{}answers.json'.format(year), encoding='utf-8') as f:
        data = json.load(f)
    for award in data['award_data'].keys():
        candidates[award] = []
        candidates[award].extend(data["award_data"][award]["nominees"])
        candidates[award].append(data["award_data"][award]["winner"])
    return candidates


def get_winner(year):
    award_mappings = get_filtered_awards(year)
    clean_awards = award_mappings.keys()
    
    potential_winners = {}
    for clean_award in clean_awards:
        potential_winners[clean_award] = Counter()

    candidates = get_candidates(year)
    awards_to_candidates = {}
    for clean_award in clean_awards:
        awards_to_candidates[clean_award] = candidates[award_mappings[clean_award]]

    # print("AWARDS TO CANDIDATES")
    # print(awards_to_candidates)

    all_tweets = get_tweets(year)
    # all_tweets = ["Jodie Fostor wins the cecil b. demille award.", "Argo wins the best motion picture in drama. Jennifer Lawrence wins the best actress performance in a motion picture drama."]
    # all_tweets = ["John Doe wins the cecil b. demille award.", "John Doe wins the cecil b. demille award.", "Johnny Doe wins the cecil b. demille award."]
    for tweet in all_tweets:
        sentences = sent_tokenize(tweet)
        people_names = []
        other_names = []
        for sentence in sentences:
            # print("NOW PARSING={}".format(sentence))
            # Start until key word
            won_index = sentence.find(' won ')
            if won_index != -1:
                tokens = word_tokenize(sentence[:won_index])
                people_names.append([sentence[won_index+5:], list(bigrams(tokens))])
                other_names.append([sentence[won_index+5:], list(everygrams(tokens, max_len=3))])

            
            wins_index = sentence.find(' wins ')
            if wins_index != -1:
                tokens = word_tokenize(sentence[:wins_index])
                people_names.append([sentence[wins_index+6:], list(bigrams(tokens))])
                other_names.append([sentence[wins_index+6:], list(everygrams(tokens, max_len=3))])
            
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
                            for candidate in awards_to_candidates[award]:
                                if Levenshtein.ratio(candidate, phrase) >= 0.6:
                                    potential_winners[award][candidate] = potential_winners[award].get(candidate, 0) + 1
            else:
                for potential_award, other_name in other_names:
                    filtered_potential_award = ' '.join([token for token in word_tokenize(potential_award) if token not in AWARD_STOP_WORDS])
                    # print("AWARD={}, POTENTIAL_AWARD={}, RATIO={}".format(award, filtered_potential_award, Levenshtein.ratio(award, filtered_potential_award)))
                    if Levenshtein.ratio(award, filtered_potential_award) >= 0.6:
                        for gram in other_name:
                            phrase = ' '.join(gram)
                            phrase = phrase.lower()
                            for candidate in awards_to_candidates[award]:
                                if Levenshtein.ratio(candidate, phrase) >= 0.6:
                                    potential_winners[award][candidate] = potential_winners[award].get(candidate, 0) + 1

    # print(potential_winners)
    winners = {}
    for award in clean_awards:
        award_name = award_mappings[award]
        # print("AWARD NAME={}".format(award_name))
        if len(potential_winners[award]) > 0:
            # print("Winner Candidates for AWARD={}, CHOSE={}".format(potential_winners[award].most_common(10), potential_winners[award].most_common(1)[0][0]))
            winners[award_name] = potential_winners[award].most_common(1)[0][0]

            # print("Winner Candidates for AWARD={}, CHOSE={}".format(collapsed_potential_winners[award].most_common(10), collapsed_potential_winners[award].most_common(1)[0][0]))
            # winners[award_name] = collapsed_potential_winners[award].most_common(1)[0][0]
        else:
            winners[award_name] = "Not found"

        # print("\n")

    # print(winners)
    return winners


# get_winner('2013')