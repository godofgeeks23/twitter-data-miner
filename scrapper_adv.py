import os
from dotenv import load_dotenv
import tweepy

consumer_key = os.getenv('consumer_key')
consumer_secret = os.getenv('consumer_secret')
access_token = os.getenv('access_token')
access_token_secret = os.getenv('access_token_secret')

client = tweepy.Client(consumer_key= consumer_key,consumer_secret= consumer_secret,access_token= access_token,access_token_secret= access_token_secret)
query = 'news'
tweets = client.search_recent_tweets(query=query, max_results=10)
for tweet in tweets.data:
    print(tweet.text)