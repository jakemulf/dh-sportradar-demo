d = None
with open("/data/daily_change_log.json", "r") as f:
    d = json.loads(f.read())
table_writers = extract_sport_radar_json_lists(d)
for key in table_writers.keys():
    globals()[f"daily_change_log_{key}"] = table_writers[key].table

with open("/data/league_leaders.json", "r") as f:
    d = json.loads(f.read())
table_writers = extract_sport_radar_json_lists(d)
for key in table_writers.keys():
    globals()[f"league_leaders_{key}"] = table_writers[key].table
