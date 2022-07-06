# dh-sportradar-demo

This sample app shows how to collect data from https://developer.sportradar.com/, both from pulling (using the REST API) and pushing (receiving webhooks from the API).

## Components

* `./data/app.d/`: The Deephaven app mode directory
  * `./data/app.d/webhook_feed.py`: The Python script to setup the webhook feed
  * `./data/app.d/app.app`: The Deephaven app mode config file
* `./data/notebooks/`: Various Python scripts to collect data from SportRadar
* `./flask_server/`: The Python project to run the server to accept the SportRadar webhooks
  * `./flask_server/requirements.txt`: The Python dependencies for the project
  * `./flask_server/server.py`: The Python Flask server
* `./docker-compose.yml`: The docker-compose file for the project

## Environmental variables

The following environmental variables need to be set for the project. `.env` is the recommended file to put the environmental variables in.

```
TOPIC_NAME
KAFKA_SERVER
REDPANDA_SERVER
```

It's recommended to use the values in `.env_sample`

```
TOPIC_NAME="test.topic"
KAFKA_SERVER="localhost:9092"
REDPANDA_SERVER="redpanda:29092"
```

## Launch

Before launching, it's recommended to setup a Python virtual environment. Run the following in your terminal to setup the virtual environment

```
python3 -m venv venv
source venv/bin/activate
```

If `python` already points to some 3.X version of python, use the following

```
python -m venv venv
source venv/bin/activate
```

To launch the app, run the following in your terminal

```
docker-compose up -d
pip install -r ./flask_server/requirements.txt
python ./flask_server/server.py
```

To stop the app, you can kill the Python command using `ctrl-c`, and then run `docker-compose stop`

## SportRadar configuration

TODO

## Using the app

This app runs Python scripts in Deephaven that set up tables to collect data from https://developer.sportradar.com/. On launch, the `webhook_table` is created and contains streaming data from the SportRadar webhooks. This data comes from a Kafka feed that the Flask server writes to. The Python scripts in the `./data/notebooks/` directory can be used to pull data from the SportRadar API and create various Deephaven artifacts using the data.

The Python Flask server contains a single route that accepts a JSON request body, and writes it to the Kafka feed that the `webhook_table` reads from.
