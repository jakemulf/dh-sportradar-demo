import requests

import os

try:
    SPORT_RADAR_API_KEY = os.environ["SPORT_RADAR_API_KEY"]
except KeyError:
    print("Set the SPORT_RADAR_API_KEY before making API requests")
    exit(1)

api_response_json = requests.get(f"http://api.sportradar.us/mlb/trial/v7/en/games/2021/REG/schedule.json?api_key={SPORT_RADAR_API_KEY}").json()
table_writers = extract_sport_radar_json(api_response_json)
for key in table_writers.keys():
    globals()[f"league_schedule_{key}"] = table_writers[key].table
