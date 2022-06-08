import os
from dotenv import load_dotenv
from pathlib import Path
import tweepy as tw
import json
import kafka  # Section 1



load_dotenv()  # Section 2

consumer_key = os.getenv("consumer_key")
consumer_secret = os.getenv("consumer_secret")
access_token = os.getenv("access_token")
access_token_secret = os.getenv("access_token_secret")  # Section 3
auth = tw.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tw.API(auth, wait_on_rate_limit=True)  # Section 4


class MyStreamListener(tw.StreamListener):
    def on_status(self, data):
        tweet_dict = {"text": data.text,
                      "user_name": data.user.name,
                      "screen_name": data.user.screen_name,
                      "id_string": data.user.id_str,
                      "location": data.user.location,
                      } 
        print(data.text)
        # THE FOLLOWING LINE SENDS DATA IN KAFKA (Under topic "trump").
        producer.send("trump", json.dumps(tweet_dict).encode("utf-8"))
        return True

    def on_error(self, status_code):
        if status_code == 420:
            return False  # Section 5


producer = kafka.KafkaProducer(bootstrap_servers="localhost: 9092")
myStreamListener = MyStreamListener()
myStream = tw.Stream(auth=api.auth, listener=myStreamListener)
myStream.filter(track=["trump"], is_async=True)
