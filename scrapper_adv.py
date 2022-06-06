import tweepy

consumer_key = "x"
consumer_secret = "x"
access_token = "x"
access_token_secret = "x"

client = tweepy.Client(consumer_key= consumer_key,consumer_secret= consumer_secret,access_token= access_token,access_token_secret= access_token_secret)
query = 'news'
tweets = client.search_recent_tweets(query=query, max_results=10)
for tweet in tweets.data:
    print(tweet.text)