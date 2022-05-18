import json
from collections import Counter
from re import A
import re
from nltk import bigrams
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.util import everygrams
from nltk.corpus import stopwords
import Levenshtein
import GenerateTweetsByAward as gtba
from helpers.tweet_preprocessing import clean

AWARD_STOP_WORDS = set(['by', 'an', 'in', 'a', 'performance', 'or', 'role', 'made', 'for', '-', ','])
TWEET_STOP_WORDS = set(["the", 'el', "golden", "globes", "for", "to", "and"])
STOPWORDS = set(stopwords.words('english'))
OFFICIAL_AWARDS = ['cecil b. demille award', 'best motion picture - drama', 'best performance by an actress in a motion picture - drama', 'best performance by an actor in a motion picture - drama', 'best motion picture - comedy or musical', 'best performance by an actress in a motion picture - comedy or musical', 'best performance by an actor in a motion picture - comedy or musical', 'best animated feature film', 'best foreign language film', 'best performance by an actress in a supporting role in a motion picture', 'best performance by an actor in a supporting role in a motion picture', 'best director - motion picture', 'best screenplay - motion picture', 'best original score - motion picture', 'best original song - motion picture', 'best television series - drama', 'best performance by an actress in a television series - drama', 'best performance by an actor in a television series - drama', 'best television series - comedy or musical', 'best performance by an actress in a television series - comedy or musical', 'best performance by an actor in a television series - comedy or musical', 'best mini-series or motion picture made for television', 'best performance by an actress in a mini-series or motion picture made for television', 'best performance by an actor in a mini-series or motion picture made for television', 'best performance by an actress in a supporting role in a series, mini-series or motion picture made for television', 'best performance by an actor in a supporting role in a series, mini-series or motion picture made for television']

# Returns dictionary mapping between KEY = clean name, VALUE = original name
def get_filtered_awards(year):
    clean_awards = {}
    for award in OFFICIAL_AWARDS:
        text_lst = word_tokenize(award)
        filtered_text_lst = [token for token in text_lst if token not in AWARD_STOP_WORDS]
        clean_awards[' '.join(filtered_text_lst)] = award
        # clean_awards[frozenset(filtered_text_lst)] = award

    return clean_awards

# def get_winner(year):
#     award_mappings = get_filtered_awards(year)
#     clean_awards = award_mappings.keys()

#     winners = {}

#     def get_winner_award(year, award, clean_award):
#         def goodgram(gram):
#             for g in gram:
#                 for sws in [award.split(' '), AWARD_STOP_WORDS, TWEET_STOP_WORDS, STOPWORDS]:
#                     for w in sws:
#                         if Levenshtein.ratio(g, w) >= 0.75:
#                             return False
#             return True

#         with open('awardsandfilters/{}{}.txt'.format(re.sub("[^a-zA-Z]", "", award),year)) as f:
#             all_tweets = f.readlines()

#             names = {}
#             for tweet in all_tweets:
#                 sentences = sent_tokenize(tweet.lower())
#                 for sentence in sentences:
#                     if any(word in clean_award for word in ["actor", "actress", "director", "demille"]):
#                         temp = list(filter(goodgram, bigrams(word_tokenize(sentence))))
#                     else:
#                         temp = list(filter(goodgram, everygrams(word_tokenize(sentence), max_len=3)))

#                     for x in temp:
#                         if x in names:
#                             names[x] += 1
#                         else:
#                             names[x] = 1

#             name = sorted(list(map(lambda x: [x, names[x]], names.keys())),\
#                 key=lambda y: -y[1])[0][0]
            
#             winners[award] = ' '.join(name)

#     for clean_award in clean_awards:
#         get_winner_award(year, award_mappings[clean_award], clean_award)

#     # print(winners)
#     return winners    

#######

def get_winner(year):
    # gtba.generateTweetsByAward(year)
    award_mappings = get_filtered_awards(year)
    clean_awards = award_mappings.keys()

    potential_winners = {}


    def get_winner_award(year, award, clean_award):
        with open('awardsandfilters/{}{}.txt'.format(re.sub("[^a-zA-Z]", "", award),year)) as f:
            all_tweets = f.readlines()

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

                    # People award, needs two names
                    if any(word in clean_award for word in ["actor", "actress", "director", "demille"]):
                        for potential_award, people_name in people_names:
                            filtered_potential_award = ' '.join([token for token in word_tokenize(potential_award) if token not in AWARD_STOP_WORDS])
                            # print("AWARD={}, POTENTIAL_AWARD={}, RATIO={}, PEOPlE_NAME={}".format(award, filtered_potential_award, Levenshtein.ratio(award, filtered_potential_award), people_name))
                            if Levenshtein.ratio(clean_award, filtered_potential_award) >= 0.6:
                                for gram in people_name:
                                    phrase = ' '.join(gram)
                                    phrase = phrase.lower()
                                    potential_winners[clean_award][phrase] = potential_winners[clean_award].get(phrase, 0) + 1
                    else:
                        for potential_award, other_name in other_names:
                            filtered_potential_award = ' '.join([token for token in word_tokenize(potential_award) if token not in AWARD_STOP_WORDS])
                            # print("AWARD={}, POTENTIAL_AWARD={}, RATIO={}".format(award, filtered_potential_award, Levenshtein.ratio(award, filtered_potential_award)))
                            if Levenshtein.ratio(clean_award, filtered_potential_award) >= 0.6:
                                for gram in other_name:
                                    phrase = ' '.join(gram)
                                    phrase = phrase.lower()
                                    potential_winners[clean_award][phrase] = potential_winners[clean_award].get(phrase, 0) + 1

    for clean_award in clean_awards:
        potential_winners[clean_award] = Counter()
        get_winner_award(year, award_mappings[clean_award], clean_award)

    collapsed_potential_winners = {}
    for clean_award in clean_awards:
        collapsed_potential_winners[clean_award] = Counter()
    
    for award in clean_awards:
        for potential_winner in potential_winners[award].keys():
            # print("Potential winner: ", potential_winner)
            added = False
            
            for collapsed_potential_winner in collapsed_potential_winners[award].keys():
                # print("POTENTIAL WINNER={}, COLLAPSED={}".format(potential_winner, collapsed_potential_winner))
                # print("CURRENT FREQ COUNT: ", collapsed_potential_winners[award][potential_winner])
                if Levenshtein.ratio(collapsed_potential_winner, potential_winner) >= 0.8:
                    # print("Ratio > 0.6")
                    collapsed_potential_winners[award][collapsed_potential_winner] += 1
                    added = True
            
            if not added:
                collapsed_potential_winners[award][potential_winner] = potential_winners[award][potential_winner]
                # print("Added: ", collapsed_potential_winners[award])
    
    winners = {}
    for award in clean_awards:
        award_name = award_mappings[award]
        # print("AWARD NAME={}".format(award_name))
        if len(collapsed_potential_winners[award]) > 0:
            # print("Winner Candidates for AWARD={}, CHOSE={}".format(potential_winners[award].most_common(10), potential_winners[award].most_common(1)[0][0]))
            # winners[award_name] = potential_winners[award].most_common(1)[0][0]

            # print("Winner Candidates for AWARD={}, CHOSE={}".format(collapsed_potential_winners[award].most_common(10), collapsed_potential_winners[award].most_common(1)[0][0]))
            winners[award_name] = collapsed_potential_winners[award].most_common(1)[0][0]
        else:
            winners[award_name] = "Not found"

        # print("\n")

    # print(winners)
    return winners    


###########
        
# def get_winner(year):
#     award_mappings = get_filtered_awards(year)
#     clean_awards = award_mappings.keys()
    
#     potential_winners = {}
#     for clean_award in clean_awards:
#         potential_winners[clean_award] = Counter()

#     all_tweets = get_tweets(year)
#     # all_tweets = ["John Doe wins the cecil b. demille award.", "Argo wins the best motion picture in drama. Jennifer Lawrence wins the best actress performance in a motion picture drama."]
#     # all_tweets = ["John Doe wins the cecil b. demille award.", "John Doe wins the cecil b. demille award.", "Johnny Doe wins the cecil b. demille award."]
#     for tweet in all_tweets:
#         sentences = sent_tokenize(tweet)
#         people_names = []
#         other_names = []
#         for sentence in sentences:
#             # print("NOW PARSING={}".format(sentence))
#             # Start until key word
#             won_index = sentence.find(' won ')
#             if won_index != -1:
#                 tokens = word_tokenize(sentence[:won_index])
#                 people_names.append([sentence[won_index+5:], list(bigrams(tokens))])
#                 other_names.append([sentence[won_index+5:], list(everygrams(tokens, max_len=3))])

            
#             wins_index = sentence.find(' wins ')
#             if wins_index != -1:
#                 tokens = word_tokenize(sentence[:wins_index])
#                 people_names.append([sentence[wins_index+6:], list(bigrams(tokens))])
#                 other_names.append([sentence[wins_index+6:], list(everygrams(tokens, max_len=3))])
            
#             # print("PEOPLE NAMES: ", people_names)
#             # print("OTHER NAMES: ", other_names)
            
#             # Start after key word

#         for award in clean_awards:
#             # People award, needs two names
#             if any(word in award for word in ["actor", "actress", "director", "demille"]):
#                 for potential_award, people_name in people_names:
#                     filtered_potential_award = ' '.join([token for token in word_tokenize(potential_award) if token not in AWARD_STOP_WORDS])
#                     # print("AWARD={}, POTENTIAL_AWARD={}, RATIO={}, PEOPlE_NAME={}".format(award, filtered_potential_award, Levenshtein.ratio(award, filtered_potential_award), people_name))
#                     if Levenshtein.ratio(award, filtered_potential_award) >= 0.6:
#                         for gram in people_name:
#                             phrase = ' '.join(gram)
#                             phrase = phrase.lower()
#                             potential_winners[award][phrase] = potential_winners[award].get(phrase, 0) + 1
#             else:
#                 for potential_award, other_name in other_names:
#                     filtered_potential_award = ' '.join([token for token in word_tokenize(potential_award) if token not in AWARD_STOP_WORDS])
#                     # print("AWARD={}, POTENTIAL_AWARD={}, RATIO={}".format(award, filtered_potential_award, Levenshtein.ratio(award, filtered_potential_award)))
#                     if Levenshtein.ratio(award, filtered_potential_award) >= 0.6:
#                         for gram in other_name:
#                             phrase = ' '.join(gram)
#                             phrase = phrase.lower()
#                             potential_winners[award][phrase] = potential_winners[award].get(phrase, 0) + 1

#     # print(potential_winners)
#     collapsed_potential_winners = {}
#     for clean_award in clean_awards:
#         collapsed_potential_winners[clean_award] = Counter()
    
#     for award in clean_awards:
#         for potential_winner in potential_winners[award].keys():
#             # print("Potential winner: ", potential_winner)
#             added = False
            
#             for collapsed_potential_winner in collapsed_potential_winners[award].keys():
#                 # print("POTENTIAL WINNER={}, COLLAPSED={}".format(potential_winner, collapsed_potential_winner))
#                 # print("CURRENT FREQ COUNT: ", collapsed_potential_winners[award][potential_winner])
#                 if Levenshtein.ratio(collapsed_potential_winner, potential_winner) >= 0.8:
#                     # print("Ratio > 0.6")
#                     collapsed_potential_winners[award][collapsed_potential_winner] += 1
#                     added = True
            
#             if not added:
#                 collapsed_potential_winners[award][potential_winner] = potential_winners[award][potential_winner]
#                 # print("Added: ", collapsed_potential_winners[award])
    
#     winners = {}
#     for award in clean_awards:
#         award_name = award_mappings[award]
#         # print("AWARD NAME={}".format(award_name))
#         if len(collapsed_potential_winners[award]) > 0:
#             # print("Winner Candidates for AWARD={}, CHOSE={}".format(potential_winners[award].most_common(10), potential_winners[award].most_common(1)[0][0]))
#             # winners[award_name] = potential_winners[award].most_common(1)[0][0]

#             # print("Winner Candidates for AWARD={}, CHOSE={}".format(collapsed_potential_winners[award].most_common(10), collapsed_potential_winners[award].most_common(1)[0][0]))
#             winners[award_name] = collapsed_potential_winners[award].most_common(1)[0][0]
#         else:
#             winners[award_name] = "Not found"

#         # print("\n")

#     # print(winners)
#     return winners


# # get_winner('2013')