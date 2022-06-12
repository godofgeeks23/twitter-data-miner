# # Frontend-Tweet

### A tool to scrape live Twitter data using Python and analyzing it using Elastic stack

##  Installation and Setup

### Installing Java

    sudo apt update

    sudo apt install default-jre

    sudo apt install default-jdk
    
### Installing nginx

    sudo apt update
    
    sudo apt install nginx
    
    sudo ufw allow 'Nginx HTTP'
    
    sudo systemctl enable nginx
    
    sudo systemctl start nginx

### Installing and Configuring Elasticsearch

    curl -fsSL https://artifacts.elastic.co/GPG-KEY-elasticsearch |sudo gpg --dearmor -o /usr/share/keyrings/elastic.gpg
    
    echo "deb [signed-by=/usr/share/keyrings/elastic.gpg] https://artifacts.elastic.co/packages/7.x/apt stable main" | sudo tee -a /etc/apt/sources.list.d/elastic-7.x.list
    
    sudo apt update
    
    sudo apt install elasticsearch

Now we will configure elasticsearch - 

    sudo nano /etc/elasticsearch/elasticsearch.yml

Find the line that specifies `network.host`, uncomment it, and replace its value with `localhost`

Save the changes by `Ctrl+X`, `Y` and Enter. 

Now start the elasticsearch service by - 

    sudo systemctl start elasticsearch

Next, run the following command to enable Elasticsearch to start up every time the server boots:

    sudo systemctl enable elasticsearch

### Installing and Configuring the Kibana Dashboard

    sudo apt install kibana
    
    sudo systemctl enable kibana
    
    sudo systemctl start kibana

Because Kibana is configured to only listen on `localhost`, we must set up a reverse proxy to allow external access to it. We will use Nginx for this purpose.

    echo "kibanaadmin:`openssl passwd -apr1`" | sudo tee -a /etc/nginx/htpasswd.users

Enter and confirm a password at the prompt. Remember or take note of this login, as you will need it to access the Kibana web interface.

Next, we will create an Nginx server block file.

    sudo nano /etc/nginx/sites-available/your_domain

Delete all existing data, and paste in the following:

    server {
        listen 80;
    
        server_name your_domain;
    
        auth_basic "Restricted Access";
        auth_basic_user_file /etc/nginx/htpasswd.users;
    
        location / {
            proxy_pass http://localhost:5601;
            proxy_http_version 1.1;
            proxy_set_header Upgrade $http_upgrade;
            proxy_set_header Connection 'upgrade';
            proxy_set_header Host $host;
            proxy_cache_bypass $http_upgrade;
        }
    }

Save and close the file.

    sudo ln -s /etc/nginx/sites-available/your_domain /etc/nginx/sites-enabled/your_domain
    
    sudo systemctl reload nginx
    
    sudo ufw allow 'Nginx Full'

Kibana is now accessible via your public IP address of your Elastic Stack server. You can check the Kibana server’s status page by navigating to the IP address and entering your login credentials when prompted.

### ## Installing and Configuring Logstash

    sudo apt install logstash

Create a logstash config file by - 

    sudo nano /etc/logstash/conf.d/kafkatwitter.conf

And paste the following content in it:

    input {
        kafka {
            topics => "trump" #your kafka should have this topic at this point.
        }
    }output {
        elasticsearch { hosts => ["localhost:9200"] index =>    "practice_index"}
        stdout { codec => "rubydebug" }
    }

Save the file.

    /usr/share/logstash/bin/logstash -f /etc/logstash/conf.d/kafkatwitter.conf

### Installing and Starting Kafka

    wget https://dlcdn.apache.org/kafka/3.2.0/kafka_2.13-3.2.0.tgz
    
    tar xzf kafka_2.13-3.2.0.tgz
    
    cd kafka_2.13-3.2.0/

Start the **ZooKeeper server** followed by the **Kafka server** by running the following commands:

    bin/zookeeper-server-start.sh config/zookeeper.properties

    bin/kafka-server-start.sh config/server.properties

Create a topic to which your system will be publishing data - 

    bin/kafka-topics.sh --create --bootstrap-server localhost:9092 --replication-factor 1 --partitions 1 --topic trump

### Setting up Python and Twitter API Credentials

Recommended Python version - `3.10.4`

Clone the repo or download the code zip file.

Navigate into the local repo, and run the command for installing dependencies - 

    pip install -r ./requirements.txt


Create a `.env` file in the directory, and set its contents as:

    consumer_key='< your consumer key >'
    
    consumer_secret='< your consumer secret >'
    
    access_token='< your access token >'
    
    access_token_secret='< your access token secret >'
    
    bearer_token='< your bearer token >'

And save it.

*The credentials can be obtained by signing up for a Twitter developer account and API access.*


## Usage

In `kafka_test_stream.py` ,  modify the line contaning 

    terms = "........"

to the topics you want data of.

Run the script by 

    python ./kafka_test_stream.py 

The data scrapping starts and is sent to Elasticsearch through Kafka and Logstash.
To view and analyze data from Kibana - 

1. Open Kibana
2. Goto Index Patterns.
3. Create a new index pattern
4. Select practice* from the available list of indexes.
5. Create pattern, go to Kibana Discover, and select that index pattern to view the data collected.
