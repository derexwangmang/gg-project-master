import re
from helpers import tweet_preprocessing as TP 

def generateTweetsByAward(year):
    tweets = TP.get_tweets(year)
    counter = 0
    output = []
    with open('awardsandfilters/awardsandfilters.txt') as f:
        lines = f.readlines()
        for l in lines:
            arr = l.split(';')
            category = arr[0]
            posfilters = arr[1][:-1] if len(arr) <= 2 else arr[1]
            posfilters = re.compile("^(?=.*" + ")(?=.*".join(posfilters.split(',')) + ").*$", re.IGNORECASE)
            filteredtweets = list(filter(posfilters.search, tweets))

            # if len(arr) > 2:
            #     negfilters = re.compile("^((?=.*" + ")|(?=.*".join(arr[2][-1].split(',')) + ")).*$", re.IGNORECASE)
            #     filteredtweets = list(filter(lambda x: not negfilters.search(x), filteredtweets))

            fi = open('awardsandfilters/{}{}.txt'.format(re.sub("[^a-zA-Z]", "", category), year), 'w')
            # fi.write('{}\n{} Tweets Found\n\n'.format(category, len(filteredtweets)))
            for i, tweet in enumerate(filteredtweets):
                fi.write(tweet + ('\n' if year==2015 else ''))
            fi.close()
            counter += 1
            output.append(len(filteredtweets))

    # print(output)
