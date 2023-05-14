import tweepy
import json
from datetime import datetime
import s3fs
import os

access_key = os.environ.get("TWITTER_API_KEY") 
access_secret = os.environ.get("TWITTER_API_SECRET")
consumer_key = os.environ.get("TWITTER_ACCESS_TOKEN")
consumer_secret = os.environ.get("TWITTER_ACCESS_TOKEN_SECRET")

def fetch_twitter_data(account):
    try:
        auth= tweepy.OAuth1UserHandler(access_key, access_secret)
        auth.set_access_token(consumer_key, consumer_secret)

        twitter_api = tweepy.API(auth)

    except tweepy.errors.Unauthorized as error:
        print(f'{error}, please check provided api secrets and keys')
    else:
        tweets = twitter_api.user_timeline(screen_name=f'@{account}', 
                        # 200 is the maximum allowed count
                        count=200,
                        include_rts = False,
                        # Necessary to keep full_text 
                        # otherwise only the first 140 words are extracted
                        tweet_mode = 'extended',
                        exclude_replies = True
                        )

        tweets_dict = {str((tweet.user.screen_name, tweet.id)):tweet._json["full_text"] for tweet in tweets}
        # print(tweets_dict.keys(),sep='\n')
        return tweets_dict
    
def write_as_json(account, dict:dict):
    try:
        with open(f"{account}.json", "w") as f:
            json.dump(dict, f)
    except IOError as e:
        print(f"Error writing JSON file: {str(e)}")


tweets_dict = fetch_twitter_data('rempuff')
write_as_json('rempuff', tweets_dict)