import tweepy as tw
import json
from dotenv import load_dotenv
import os

load_dotenv()

twitter_cred = dict()
twitter_cred["CONSUMER_KEY"] = os.getenv('consumer_key')
twitter_cred["CONSUMER_SECRET"] = os.getenv('consumer_secret')
twitter_cred["ACCESS_KEY"] = os.getenv('access_token')
twitter_cred["ACCESS_SECRET"] = os.getenv('access_token_secret')

auth = tw.OAuthHandler(
    twitter_cred["CONSUMER_KEY"], twitter_cred["CONSUMER_SECRET"])
auth.set_access_token(
    twitter_cred["ACCESS_KEY"], twitter_cred["ACCESS_SECRET"])
api = tw.API(auth, wait_on_rate_limit=True)


class StreamAPI(tw.StreamingClient):
    def on_data(self, raw_data):
        json_data = json.loads(raw_data)
        # with open("json_data.json", "w") as f:
            # json.dump(json_data, f)
        print(raw_data)
        print()
        # producer.send("trump", json.dumps(json_data).encode("utf-8"))
        # return True

# producer = kafka.KafkaProducer(bootstrap_servers="localhost:9092")

streamer = StreamAPI(os.getenv('bearer_token'))

# terms = "#Darkweb OR #Criminal OR #Intelligence OR #OSINT OR #DeepWeb OR #Leaked OR #DataBreach OR #Terror OR #Drugs OR #Cryptocurrency OR #Ransomware OR #carding OR #onionlink"
terms = "from:godofgeeks_"

# for rule in streamer.get_rules().data:
#     streamer.delete_rules(rule.id)
# print(streamer.get_rules())

streamer.add_rules(tw.StreamRule(terms))
streamer.filter()
