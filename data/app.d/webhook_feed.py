"""
webhook_feed.py

A Deephaven app mode script that sets up the webhook table that reads from a Kafka feed
"""
from deephaven.stream.kafka import consumer as kt

import os

try:
    TOPIC_NAME = os.environ["TOPIC_NAME"]
    REDPANDA_SERVER = os.environ["REDPANDA_SERVER"]
except KeyError:
    sys.exit("Please set the proper environmental variables defined in the README")

webhook_table = kt.consume({'bootstrap.servers': REDPANDA_SERVER},
                        TOPIC_NAME, table_type=kt.TableType.append(),
                        key_spec=kt.KeyValueSpec.IGNORE)
