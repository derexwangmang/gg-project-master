import json
import re
from collections import Counter

def get_hosts(tweets):
    host_discussion_pattern = re.compile('hosted|hosting')
    host_relevant_tweets = list(filter(host_discussion_pattern.search, tweets))

    host_multiple_names_pattern = re.compile('[A-Z][a-z]+ [A-Z][a-z]+ (and|&) [A-Z][a-z]+ [A-Z][a-z]+')
    host_mention_tweets = list(filter(host_multiple_names_pattern.search, host_relevant_tweets))

    host_name_pattern = re.compile('[A-Z][a-z]+ [A-Z][a-z]+')
    host_names = Counter()
    for tweet in host_mention_tweets:
        potential_names = host_name_pattern.findall(tweet)
        host_names.update(potential_names)
    
    hosts = []
    top_hosts = host_names.most_common(2)
    for name, _ in top_hosts:
        hosts.append(name)
    
    return hosts