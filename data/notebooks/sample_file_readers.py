d = None
with open("/data/sample_json/daily_change_log.json", "r") as f:
    d = json.loads(f.read())
table_writers = extract_sport_radar_json(d)
for key in table_writers.keys():
    globals()[f"daily_change_log_{key}"] = table_writers[key].table

#NOTE: This section takes a while to run. If you want a quick demo, feel free to omit this section
with open("/data/sample_json/league_leaders.json", "r") as f:
    d = json.loads(f.read())
table_writers = extract_sport_radar_json(d)
for key in table_writers.keys():
    globals()[f"league_leaders_{key}"] = table_writers[key].table
