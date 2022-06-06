# OAuth2.0 Version 
import tweepy
import json

client = tweepy.Client(bearer_token='x')

query = 'trump -is:retweet lang:en'
tweets = tweepy.Paginator(client.search_recent_tweets, query=query,
                              tweet_fields=['context_annotations', 'created_at'], max_results=10).flatten(limit=1)

# print(tweets.keys())
for tweet in tweets:
    # print(tweet.created_at)
    print(tweet.text)
    # print(dir(tweet))
    # print(tweet.like_count)

    # if len(tweet.context_annotations) > 0:
        # print(tweet.context_annotations)
        # print()
# z = [x.toJSON() for x in tweets]
# with open('your_data.json', 'w') as out:
    # json.dump(z,out)
    # out.write(tweets)