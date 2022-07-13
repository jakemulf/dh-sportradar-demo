from deephaven.time import to_datetime
from dateutil import parser

import re

def datetime_converter(datetime_str):
    match = re.match(r'(\d{4})-(\d{2})-(\d{2})T(\d{2}):(\d{2}):(\d{2})', datetime_str)
    
    if not bool(match):
        return None

    try:
        dt = parser.parse(datetime_str)
        dts = dt.strftime("%Y-%m-%dT%H:%M:%S") + " UTC"
        return to_datetime(dts)
    except:
        return None

d = None
with open("/data/sample_json/daily_change_log.json", "r") as f:
    d = json.loads(f.read())
table_writers = extract_sport_radar_json(d)
for key in table_writers.keys():
    globals()[f"daily_change_log_{key}"] = table_writers[key].create_table()

with open("/data/sample_json/transactions.json", "r") as f:
    d = json.loads(f.read())
table_writers = extract_sport_radar_json(d)
for key in table_writers.keys():
    globals()[f"transactions_{key}"] = table_writers[key].create_table()

d = None
with open("/data/sample_json/play_by_play.json", "r") as f:
    d = json.loads(f.read())
table_writers = extract_sport_radar_json(d, datetime_converter=datetime_converter)
for key in table_writers.keys():
    globals()[f"play_by_play_{key}"] = table_writers[key].create_table()

#NOTE: This section takes a while to run, which is why it doesn't run by default. You can
#change run_long_section to True to run it
run_long_section = False
if run_long_section:
    with open("/data/sample_json/league_leaders.json", "r") as f:
        d = json.loads(f.read())
    table_writers = extract_sport_radar_json(d)
    for key in table_writers.keys():
        globals()[f"league_leaders_{key}"] = table_writers[key].create_table()
