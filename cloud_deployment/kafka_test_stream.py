import tweepy as tw
from datetime import datetime as dt
from elasticsearch import Elasticsearch
import pprint
import json
from dotenv import load_dotenv
import os
import kafka 

load_dotenv()

twitter_cred = dict()
twitter_cred["CONSUMER_KEY"] = os.getenv('consumer_key')
twitter_cred["CONSUMER_SECRET"] = os.getenv('consumer_secret')
twitter_cred["ACCESS_KEY"] = os.getenv('access_token')
twitter_cred["ACCESS_SECRET"] = os.getenv('access_token_secret')

auth = tw.OAuthHandler(twitter_cred["CONSUMER_KEY"], twitter_cred["CONSUMER_SECRET"])
auth.set_access_token(twitter_cred["ACCESS_KEY"], twitter_cred["ACCESS_SECRET"])
api = tw.API(auth, wait_on_rate_limit=True)

# Initialize elasticsearch node
# es = Elasticsearch("http://localhost:9200")

class StreamAPI(tw.StreamingClient):
    def on_data(self,raw_data):
        #if(tweet != None):
        json_data = json.loads(raw_data)
        #with open("json_data.json","w") as f:
            #json.dump(json_data,f)
        print(json_data)
        # es.index(index ="twitter_index",document=json_data,ignore=400)

        # experimental section
        producer.send("trump", json.dumps(json_data).encode("utf-8"))
        return True

producer = kafka.KafkaProducer(bootstrap_servers="localhost:9092")

streamer = StreamAPI(os.getenv('bearer_token'))

terms = "trump"

streamer.add_rules(tw.StreamRule(terms)
streamer.filter()
