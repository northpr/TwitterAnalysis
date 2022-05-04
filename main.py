import json
import pymongo
from pymongo import MongoClient
import configparser
import pandas as pd
import tweepy
import configparser
import twitter
import pprint


# Save database connection info and API Keys in a config.ini file
config = configparser.ConfigParser()
config.read('config.ini')

api_key = config['mytwitter']['api_key']
api_key_secret = config['mytwitter']['api_key_secret']

access_token = config['mytwitter']['access_token']
access_token_secret = config['mytwitter']['access_token_secret']

mongo_connect = config['mymongo']['connection']


## Authorize API
_auth = tweepy.OAuthHandler(api_key, api_key_secret)
_auth.set_access_token(access_token, access_token_secret)

tt_api = tweepy.API(_auth) #strem_api

# # Test connection works normally
# public_tweets = tt_api.home_timeline()
# print(public_tweets)

# MongoDB Compass connection
# client = pymongo.MongoClient('localhost',27017) # MongoDB connection
# twit_db = client['twitter'] # Create 'twit_db' Database - Database name 'twitter'
# twit_col = twit_db['covid'] # Create 'twit_col' Collection - Collection name 'covid'
# twit_col.create_index([("id", pymongo.ASCENDING)], unique=True)


# ## Connect to the MongoDB Cluster
client = pymongo.MongoClient()
twit_db = client['twitter']  # Create 'twit_db' Database - Database name 'twitter'
twit_col = twit_db['covid']  # Create 'twit_col' Collection - Collection name 'covid'
twit_col.create_index([("id", pymongo.ASCENDING)], unique=True)


# Define the query
search_words = ['covid']


### Use the REST API to collect tweets
## Authorize restapi
verify = tt_api.verify_credentials()


## Define the query - collect current date {for testing collect 100 tweeys}

search_results = tweepy.Cursor(tt_api.search_tweets, q="#datajobs",lang="en",
                       tweet_mode="extended").items(500) # set parameter to 500

json_data = []
for post in search_results:
    try:
        # print(post.text) # test the
        json_data.append(post._json)
    except:
        print(f'Error occured')




# # loading data into json file
# with open('tweets.json', 'w') as json_file:
#     json.dump(json_data, json_file)

twit_col.insert_many(json_data)
#


