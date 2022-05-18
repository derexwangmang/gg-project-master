import json
from collections import Counter
from re import A
import re
from nltk import bigrams
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.util import everygrams
import Levenshtein
import GenerateTweetsByAward as gtba
from helpers.tweet_preprocessing import clean
from nltk.corpus import stopwords
from nltk.corpus import names
import nltk
nltk.download('names')

AWARD_STOP_WORDS = set(['by', 'an', 'in', 'a', 'performance', 'or', 'role', 'made', 'for', '-', ','])
TWEET_STOP_WORDS = set(stopwords.words('english'))
TWEET_STOP_WORDS.update(["the", "golden", "globes", "for", "to", "and"])
TWEET_STOP_WORDS.remove("should")
TWEET_STOP_WORDS.remove("of")
TWEET_STOP_WORDS.update(["congrats", "series"])

PEOPLE_NAMES = set(names.words('male.txt'))
PEOPLE_NAMES.update(set(names.words('female.txt')))

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
    gtba.generateTweetsByAward(year)
    award_mappings = get_filtered_awards(year)
    clean_awards = award_mappings.keys()

    potential_nominees = {}

    def get_nominee_award(year, award, clean_award):
        with open('awardsandfilters/{}{}.txt'.format(re.sub("[^a-zA-Z]", "", award),year)) as f:
            all_tweets = f.readlines()

            for tweet in all_tweets:
                # print("ORIGINAL TWEET={}".format(tweet))
                # print(word_tokenize(clean_award))
                tweet = ' '.join([token for token in word_tokenize(tweet) if token.lower() not in TWEET_STOP_WORDS and token.lower() not in set(word_tokenize(clean_award))])
                titles = re.compile('[A-Z][a-z]+')
                # potential_nominees = re.findall(titles, tweet)
                # Filter out tweets talking about winner
                # if 'winner' in tweet or "wins" in tweet or "goes" in tweet or "won" in tweet:
                # print("TWEET", tweet)
                # if 'should' not in tweet or 'wish' not in tweet or 'nom' not in tweet or 'robbed' not in tweet:
                    # break
                # print("PASSED FILTER")
                # print("CLEAN AWARD: ", clean_award)
                # print("NEW TWEET={}".format(tweet))
                sentences = sent_tokenize(tweet)
                people_names = []
                other_names = []
                for sentence in sentences:
                    # print("NOW PARSING={}".format(sentence))
                    # Start until key word
                    # won_index = sentence.find(' won ')
                    # if won_index != -1:
                    #     tokens = word_tokenize(sentence[:won_index])
                        # people_names.append([sentence[won_index+5:], list(bigrams(tokens))])
                    #     other_names.append([sentence[won_index+5:], list(everygrams(tokens, max_len=3))])

                    
                    # wins_index = sentence.find(' wins ')
                    # if wins_index != -1:
                    #     tokens = word_tokenize(sentence[:wins_index])
                    #     people_names.append([sentence[wins_index+6:], list(bigrams(tokens))])
                    #     other_names.append([sentence[wins_index+6:], list(everygrams(tokens, max_len=3))])

                    nominee_candidate = re.findall(titles, tweet)
                    # tokens = word_tokenize(sentence)
                    people_names.append([sentence, list(bigrams(nominee_candidate))])
                    # print(list(bigrams(nominee_candidate)))

                    tweet_without_people_names = ' '.join([token for token in word_tokenize(tweet) if token not in PEOPLE_NAMES])
                    nominee_candidate = re.findall(titles, tweet_without_people_names)
                    other_names.append([sentence, list(everygrams(nominee_candidate, max_len=3))])


                    # for award in clean_awards:
                    # People award, needs two names
                    if any(word in clean_award for word in ["actor", "actress", "director", "demille"]):
                        for potential_award, people_name in people_names:
                            # filtered_potential_award = ' '.join([token for token in word_tokenize(potential_award) if token not in AWARD_STOP_WORDS])
                            # print("AWARD={}, POTENTIAL_AWARD={}, RATIO={}, PEOPlE_NAME={}".format(award, filtered_potential_award, Levenshtein.ratio(award, filtered_potential_award), people_name))
                            # if Levenshtein.ratio(clean_award, filtered_potential_award) >= 0.6:
                                for gram in people_name:
                                    phrase = ' '.join(gram)
                                    phrase = phrase.lower()
                                    potential_nominees[clean_award][phrase] = potential_nominees[clean_award].get(phrase, 0) + 1
                    else:
                        for potential_award, other_name in other_names:
                            # filtered_potential_award = ' '.join([token for token in word_tokenize(potential_award) if token not in AWARD_STOP_WORDS])
                            # print("AWARD={}, POTENTIAL_AWARD={}, RATIO={}".format(award, filtered_potential_award, Levenshtein.ratio(award, filtered_potential_award)))
                            # if Levenshtein.ratio(clean_award, filtered_potential_award) >= 0.6:
                                for gram in other_name:
                                    phrase = ' '.join(gram)
                                    phrase = phrase.lower()
                                    potential_nominees[clean_award][phrase] = potential_nominees[clean_award].get(phrase, 0) + 1

    for clean_award in clean_awards:
        potential_nominees[clean_award] = Counter()
        get_nominee_award(year, award_mappings[clean_award], clean_award)

    collapsed_potential_nominees = {}
    for clean_award in clean_awards:
        collapsed_potential_nominees[clean_award] = Counter()
    
    for award in clean_awards:
        for potential_nominee in potential_nominees[award].keys():
            # print("Potential nominee: ", potential_nominee)
            added = False
            
            for collapsed_potential_nominee in collapsed_potential_nominees[award].keys():
                # print("POTENTIAL nominee={}, COLLAPSED={}".format(potential_nominee, collapsed_potential_nominee))
                # print("CURRENT FREQ COUNT: ", collapsed_potential_nominees[award][potential_nominee])
                if Levenshtein.ratio(collapsed_potential_nominee, potential_nominee) >= 0.8:
                    # print("Ratio > 0.6")
                    collapsed_potential_nominees[award][collapsed_potential_nominee] += 1
                    added = True
            
            if not added:
                collapsed_potential_nominees[award][potential_nominee] = potential_nominees[award][potential_nominee]
                # print("Added: ", collapsed_potential_nominees[award])
    
    nominees = {}
    for award in clean_awards:
        award_name = award_mappings[award]
        # print("AWARD NAME={}".format(award_name))
        if len(collapsed_potential_nominees[award]) > 0:
            # print("nominee Candidates for AWARD={}, CHOSE={}".format(potential_nominees[award].most_common(10), potential_nominees[award].most_common(1)[0][0]))
            # nominees[award_name] = potential_nominees[award].most_common(1)[0][0]

            # print("nominee Candidates for AWARD={}, CHOSE={}".format(collapsed_potential_nominees[award].most_common(10), collapsed_potential_nominees[award].most_common(1)[0][0]))
            nominees[award_name] = []
            # Ignore most frequent phrase (might be winner)
            for nominee in collapsed_potential_nominees[award].most_common(4)[1:]:
                nominees[award_name].append(nominee[0])
                # if len(nominees) < 5:
                #     nominees[award_name].append(nominee[0])
                
                # if previous_count > nominee[1] * 2 or len(nominees) > 5:
                #     break
                
                # previous_count = nominee[1]
            # nominees[award_name] = [collapsed_potential_nominees[award].most_common(1)[0][0]]
        else:
            nominees[award_name] = ["Not found"]

        # print("\n")

    # print("Nominees found ", nominees)
    return nominees