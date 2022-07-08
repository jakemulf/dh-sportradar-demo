from deephaven import DynamicTableWriter
import deephaven.dtypes as dht

def extract_sport_radar_json(json_response, keys=None, dtw=None):
    """
    Extracts primitive data from a SportRadar API JSON response into Deephaven tables

    Parameters:
        json_response (dict|list|any): The SportRadar API JSON response as a Python dictionary, list, or other value
        keys (list<str>): A list of strings representing the previous keys that got to the current d
        dtw (DynamicTableWriter): The DynamicTableWriter for the table
    Returns:
        Table: The table containing all the data
    """
    if dtw is None:
        dtw_columns = {
            "Key": dht.string,
            "Value": dht.string
        }
        dtw = DynamicTableWriter(dtw_columns)
    if keys is None:
        keys = []

    if isinstance(json_response, dict):
        for key in json_response.keys():
            extract_sport_radar_json(json_response[key], keys=keys+[key], dtw=dtw)
    elif isinstance(json_response, list):
        for i in range(len(json_response)):
            extract_sport_radar_json(json_response[i], keys=keys+[str(i)], dtw=dtw)
    else:
        dtw.write_row("_".join(keys), str(json_response))

    return dtw.table

"""
Work in progress
def extract_sport_radar_json_two(json_response, keys=None, dict_tables=None):
    if dict_tables is None:
        dict_tables = {}
    if keys is None:
        keys = []

    if isinstance(json_response, dict):
        for key in json_response.keys():
            extract_sport_radar_json_two(json_response[key], keys=keys+[key], dict_tables=dict_tables)
    elif isinstance(json_response, list):
        for i in range(len(json_response)):
            extract_sport_radar_json_two(json_response[i], keys=keys+[int(i)], dict_tables=dict_tables)
    else:
        is_list = len(keys) >= 2 and isinstance(keys[-2], int)
        if is_list:
            dict_tables_key = tuple(keys[0:-2])
        else:
            dict_tables_key = tuple(keys[0:-1])
        if len(dict_tables_key) == 0:
            dict_tables_key = "meta"

        if not dict_tables_key in dict_tables:
            if is_list:
                dict_tables[dict_tables_key] = []
            else:
                dict_tables[dict_tables_key] = {}

        if is_list:
            list_index = keys[-2]
            if len(dict_tables[dict_tables_key]) <= list_index:
                dict_tables[dict_tables_key].append([])
            dict_tables[dict_tables_key][list_index].append(str(json_response))
        else:
            last_key = keys[-1]
            dict_tables[dict_tables_key][last_key] = str(json_response)

    return dict_tables
"""
