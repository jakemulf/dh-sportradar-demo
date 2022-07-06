from flask import Flask, request
from confluent_kafka import Producer
from dotenv import load_dotenv

load_dotenv()

import os
import sys

app = Flask(__name__)

try:
    TOPIC_NAME = os.environ["TOPIC_NAME"]
    KAFKA_SERVER = os.environ["KAFKA_SERVER"]
except KeyError:
    sys.exit("Please set the proper environmental variables defined in the README")

producer = Producer({
    "bootstrap.servers": KAFKA_SERVER,
})
@app.route("/", methods=["POST"])
def handle_webhook():
    data = request.data.decode("utf-8")

    producer.produce(topic=TOPIC_NAME, key=None, value=data)
    producer.flush()
    return "success"

if __name__ == '__main__':
    app.run(port=5000)
