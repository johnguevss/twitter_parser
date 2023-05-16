import tweepy
import json
from datetime import datetime
import s3fs
from configurations.config import *

def fetch_twitter_data(account):
    try:
        auth= tweepy.OAuth1UserHandler(access_key, access_secret)
        auth.set_access_token(consumer_key, consumer_secret)

        twitter_api = tweepy.API(auth)

    except tweepy.errors.Unauthorized as error:
        print(f'{error}, please check provided api secrets and keys')
    else:
        tweets = twitter_api.user_timeline(screen_name=f'@{account}', 
                        count=200,
                        include_rts = False,
                        tweet_mode = 'extended',
                        exclude_replies = True
                        )

        tweets_dict = {str((tweet.user.screen_name, tweet.id)):tweet._json["full_text"] for tweet in tweets}
        # print(tweets_dict.keys(),sep='\n')
        return tweets_dict
    
def write_as_json(account, dict:dict):
    try:
        with open(f"{MY_S3_BUCKET}/{account}.json", "w") as f:
            json.dump(dict, f)
    except IOError as e:
        print(f"Error writing JSON file: {str(e)}")

def twitter_app(account):
    tweets_dict = fetch_twitter_data(account)
    write_as_json(account, tweets_dict)

