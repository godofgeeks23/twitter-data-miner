import tweepy as tw
import json
from dotenv import load_dotenv
import os
import pygsheets

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

for rule in streamer.get_rules().data:
    streamer.delete_rules(rule.id)
print(streamer.get_rules())

rules = []
# rules.append("#Darkweb OR #Criminal OR #Intelligence OR #OSINT OR #DeepWeb OR #Leaked OR #DataBreach OR #Terror OR #Drugs OR #Cryptocurrency OR #Ransomware OR #carding OR #onionlink")
rules.append("from:godofgeeks_")

gc = pygsheets.authorize(
    service_file='verified-security-sources-6b7e7530d6f5.json')
sh = gc.open_by_url(
    "https://docs.google.com/spreadsheets/d/1ELBSsc5tQIjZFHCmTofbwflOx37CK0OOpXEiMa2Irto/edit?usp=sharing")
first_column_data = sh[0].get_col(1, include_tailing_empty=False)[1:]
usernames_list = [row.replace('https://twitter.com/', 'from:')
                  for row in first_column_data]
username_rule = " OR ".join(usernames_list)

rules.append(username_rule)

for rule in rules:
    streamer.add_rules(tw.StreamRule(rule))

streamer.filter()
