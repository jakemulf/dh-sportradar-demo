# dh-sportradar-demo

This sample app shows how to collect data from https://developer.sportradar.com/, both from pulling (using the REST API) and pushing (receiving webhooks from the API).

## Components

* `./data/app.d/`: The Deephaven app mode directory
  * `./data/app.d/webhook_feed.py`: The Python script to setup the webhook feed
  * `./data/app.d/historical_data_parser.py`: The Python script to setup pulling and parsing historical data
  * `./data/app.d/app.app`: The Deephaven app mode config file
* `./data/sample_json/`: Sample JSON files from the SportRadar API to work with without making API requests
* `./data/notebooks/`: Various Python scripts to work more with the data from SportRadar
* `./flask_server/`: The Python project to run the server to accept the SportRadar webhooks
  * `./flask_server/requirements.txt`: The Python dependencies for the flask server
  * `./flask_server/server.py`: The Python Flask server
* `./docker-compose.yml`: The docker-compose file for the project
* `Dockerfile`: The custom Dockerfile that extends the Deephaven base image
* `requirements.txt`: The Python dependencies for the Deephaven project

## Environmental variables

The following environmental variables need to be set for the project. `.env` is the recommended file to put the environmental variables in.

```
TOPIC_NAME
KAFKA_SERVER
REDPANDA_SERVER
SPORT_RADAR_API_KEY
```

It's recommended to start with the values in `.env_sample`. You can use these values by running `cp .env_sample .env`, then manually edit the file to add the `SPORT_RADAR_API_KEY` value.

## Launch

### Deephaven

To launch the Deephaven app, run the following in your terminal:

```
docker-compose up -d
```

To stop the Deephaven app, run the following:

```
docker-compose stop
```

### Python Flask server

Before launching the Python Flask server, it's recommended to setup a Python virtual environment. Run the following in your terminal to setup the virtual environment:

```
python3 -m venv venv
source venv/bin/activate
```

If `python` already points to some 3.X version of python, use the following:

```
python -m venv venv
source venv/bin/activate
```

To launch the Python flask server, run the following in your terminal:

```
pip install -r ./flask_server/requirements.txt
python ./flask_server/server.py
```

To stop the app, you can kill the Python command using `ctrl-c`.

## SportRadar configuration

Start off by going to https://developer.sportradar.com/ and click `Register`. Fill out the forum, and then activate your account with the confirmation email.

Once you can log in, go back to https://developer.sportradar.com/ and go to `My Account`, and then `Applications`. On this page, give your application a name, and then select the key(s) for the various services you want to use.

Once you get your application created, save your key in the `.env` file.

If you want to use multiple application keys, add more entries in the `.env` file and the `docker-compose.yml` file.

## Using the app

This app runs Python scripts in Deephaven that set up tables to collect data from https://developer.sportradar.com/. On launch, the `webhook_table` is created and contains streaming data from the SportRadar webhooks. This data comes from a Kafka feed that the Flask server writes to.

The Python Flask server contains a single route that accepts a JSON request body, and writes it to the Kafka feed that the `webhook_table` reads from.

The Deephaven Application Mode scripts define a method called `extract_sport_radar_json` that takes a JSON response from the SportRadar API and turns it into Deephaven tables. The Python scripts in the `./data/notebooks/` directory show how to use this method. You can use these tables to create various Deephaven artifacts (such as plots) using the data.
