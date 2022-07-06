from deephaven import DynamicTableWriter
import deephaven.dtypes as dht

import json

def extract_sport_radar_json_lists(d, response_dictionary=None, parent_keys=None):
    """
    An attempt to extract lists in the SportRadar API JSON response into useable Deephaven tables.
    The rules are as follows:
        1) Non list items are dumped into a general meta table
        2) List items are dumped into their own JSON tables

    Parameters:
        d (dict): The SportRadar API JSON response as a Python dictionary
        response_dictionary (dict): The response_dictionary used to store info for recursive calls
        parent_keys (list<str>): The JSON keys that led to the current dictionary in recursive calls
    Returns:
        dict<str, DynamicTableWriter>: Key value pairs that map to Deephaven table writers
    """
    if response_dictionary is None:
        dtw_columns = {
            "Key": dht.string,
            "Value": dht.string
        }
        dtw = DynamicTableWriter(dtw_columns)

        response_dictionary = {}
        response_dictionary["meta"] = dtw

    if parent_keys is None:
        parent_keys = []

    for key in d.keys():
        #If dictionary, simply recurse with the new key appended to parent_keys
        if isinstance(d[key], dict):
            extract_sport_radar_json_lists(d[key], response_dictionary, parent_keys + [key])

        #If list, create a new table
        elif isinstance(d[key], list):
            dtw_columns = {
                "Value": dht.string
            }
            dtw = DynamicTableWriter(dtw_columns)

            rd_key = "_".join(parent_keys + [key])
            response_dictionary[rd_key] = dtw
            for row in d[key]:
                dtw.write_row([json.dumps(row)])

        #If primitive, append it to the meta table
        else:
            meta_key = "_".join(parent_keys + [key])
            response_dictionary["meta"].write_row((meta_key, json.dumps(d[key])))

    return response_dictionary
