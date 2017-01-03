import tweepy
from datetime import tzinfo

# Replace the API_KEY and API_SECRET with your application's key and secret.
auth = tweepy.AppAuthHandler('your key','your key')
 
api = tweepy.API(auth, wait_on_rate_limit=True,
                   wait_on_rate_limit_notify=True)
 
if (not api):
    print ("Can't Authenticate")
    sys.exit(-1)
 
# Continue with rest of code

import sys
import jsonpickle
import os
import json
import pytz
from datetime import datetime
from datetime import timedelta
from time import time
from dateutil import parser
#from urllib.parse import urlparse

def set_default(obj):
    if isinstance(obj, set):
        return list(obj)
    raise TypeError


searchQuery = 'christmas -filter:retweets'  # this is what we're searching for
maxTweets = 100# Some arbitrary large number
tweetsPerQry = 100# this is the max the API permits
fName = 'abc.json' # We'll store the tweets in a text file.


# If results from a specific ID onwards are reqd, set since_id to that ID.
# else default to no lower limit, go as far back as API allows
sinceId = None

# If results only below a specific ID are, set max_id to that ID.
# else default to no upper limit, start from the most recent tweet matching the search query.
max_id = 0

tweetCount = 0
print("Downloading max {0} tweets".format(maxTweets))
with open(fName, 'w') as f:
    while tweetCount < maxTweets:
        try:
            if (max_id <= 0):
                if (not sinceId):
                    new_tweets = api.search(q=searchQuery, count=tweetsPerQry,
                                            since_id=sinceId,lang="en")
                else:
                    new_tweets = api.search(q=searchQuery, count=tweetsPerQry,
                                            since_id=sinceId,lang="en")
            else:
                if (not sinceId):
                    new_tweets = api.search(q=searchQuery, count=tweetsPerQry,
                                            max_id=str(max_id - 1),lang="en")
                else:
                    new_tweets = api.search(q=searchQuery, count=tweetsPerQry,
                                            max_id=str(max_id - 1),
                                            since_id=sinceId,lang="en")
            if not new_tweets:
                print("No more tweets found")
                break
            for tweet in new_tweets:
                #json_tweet=json.dumps(tweet)
                #jdata=json.loads(json_tweet)
                #if not 'retweeted_status' in json_tweet:
                f.write(jsonpickle.encode(tweet._json, unpicklable=False) + '\n')
                #entry={"topics": "Entertainment"}
                #d= datetime.strptime(json_tweet['created_at'], '%a %b %d %H:%M:%S +0000 %Y').replace(tzinfo=pytz.UTC)
                #json_tweet['created_at']= d.strftime('%Y-%m-%dT%H:%M:%SZ')
                
                #json_tweet.update(entry)
                #json.dump(jdata,f)
                #f.write('\n')
              
            
            tweetCount += len(new_tweets)
            print("Downloaded {0} tweets".format(tweetCount))
            max_id = new_tweets[-1].id
        except tweepy.TweepError as e:
            # Just exit if any error
            print("some error : " + str(e))
            break
    f.close()   

print ("Downloaded {0} tweets, Saved to {1}".format(tweetCount, fName))
