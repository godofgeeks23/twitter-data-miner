import tweepy
import pandas as pd
from dotenv import load_dotenv
import os

load_dotenv()

access_token = os.getenv('access_token')
access_token_secret = os.getenv('access_token_secret')
api_key = os.getenv('consumer_key')
api_key_secret = os.getenv('consumer_secret')
auth = tweepy.OAuthHandler(api_key, api_key_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

keywords = 'python javascript'
limit = 200
tweets = tweepy.Cursor(api.search_tweets, q=keywords, count=limit, tweet_mode='extended').items(limit)
# columns = ['User', 'Tweet']
# data = []
for tweet in tweets:
    # data.append([tweet.user.screen_name, tweet.full_text])
    print(tweet.user.screen_name, tweet.created_at)
    print(tweet.full_text.encode("utf-8"))
    print()
# df = pd.DataFrame(data, columns=columns)
# print(df)

# users = ['MehranShakarami', 'veritasium']
# for user in users:
#     tweets = api.user_timeline(screen_name=user,count=200,include_rts = False,tweet_mode = 'extended')
#     for info in tweets:
#         print(info.created_at)
#         print(info.full_text)

# class Linstener(tweepy.Stream):
#     tweets = []
#     limit = 1
#     def on_status(self, status):
#         self.tweets.append(status)
#         # print(status.user.screen_name + ": " + status.text)
#         if len(self.tweets) == self.limit:
#             self.disconnect()
# stream_tweet = Linstener(api_key, api_key_secret, access_token, access_token_secret)

# stream by keywords
# keywords = ['2022', '#python']
# stream_tweet.filter(track=keywords)

# # stream by users
# users = ['MehranShakarami', 'veritasium']
# user_ids = []
# for user in users:
#     user_ids.append(api.get_user(screen_name=user).id)
# stream_tweet.filter(follow=user_ids)

# columns = ['User', 'Tweet']
# data = []
# for tweet in stream_tweet.tweets:
#     if not tweet.truncated:
#         data.append([tweet.user.screen_name, tweet.text])
#     else:
#         data.append([tweet.user.screen_name, tweet.extended_tweet['full_text']])
# df = pd.DataFrame(data, columns=columns)
# print(df)