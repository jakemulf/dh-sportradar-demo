from deephaven import DynamicTableWriter
import deephaven.dtypes as dht

import json

def extract_sport_radar_json(d, response_dictionary=None, parent_keys=None, table_to_write=None):
    """
    Extracts data from a SportRadar API JSON response into Deephaven tables

    Parameters:
        d (dict|list): The SportRadar API JSON response as a Python dictionary or list
        response_dictionary (dict): The response_dictionary used to store info for recursive calls
        parent_keys (list<str>): The JSON keys that led to the current dictionary in recursive calls
        table_to_write (str): The key in the response_dictionary to write to
    Returns:
        dict<str, DynamicTableWriter>: Key value pairs that map to Deephaven table writers
    """
    if response_dictionary is None:
        response_dictionary = {}
    if table_to_write is None:
        table_to_write = "meta"
    if parent_keys is None:
        parent_keys = ["meta"]

    iter_ = None
    if isinstance(d, dict):
        iter_ = d.keys()
    elif isinstance(d, list):
        iter_ = range(len(d))

    write_values = {}
    for key in iter_:
        #If dictionary, simply recurse with the new key appended to parent_keys
        if isinstance(d[key], dict):
            new_parent_keys = parent_keys[0:-1] + [parent_keys[-1] + f"_{key}"]
            extract_sport_radar_json(d[key], response_dictionary, new_parent_keys, table_to_write)
        #If list, recurse with with the new key appended to parent_keys and a new table to write
        elif isinstance(d[key], list):
            extract_sport_radar_json(d[key], response_dictionary, parent_keys + [key], table_to_write + f"_{str(key)}")
        #If primitive, write it
        else:
            write_values[key] = str(d[key])

    if len(write_values) > 0:
        if not table_to_write in response_dictionary.keys():
            dtw_columns = {}
            last_write = None
            for parent_key in parent_keys:
                if isinstance(parent_key, str):
                    dtw_columns[parent_key] = dht.string
                    last_write = parent_key
                #We shouldn't get an int as the first item, could be fixed though
                elif isinstance(parent_key, int):
                    dtw_columns[last_write] = dht.int_
            for write_key in write_values.keys():
                dtw_columns[write_key] = dht.string

            dtw = DynamicTableWriter(dtw_columns)
            response_dictionary[table_to_write] = dtw

        parent_keys_to_write = []
        for parent_key in parent_keys:
            #If an int is found, the previous value is its identifier, we don't
            #need to write the identifier of an int (since it's in the column name),
            #just the index
            if isinstance(parent_key, int):
                parent_keys_to_write[-1] = parent_key
            else:
                parent_keys_to_write.append(parent_key)

        row_to_write = parent_keys_to_write + [write_values[write_key] for write_key in write_values.keys()]
        try:
            response_dictionary[table_to_write].write_row(row_to_write)
        except:
            pass #BAD, REMOVE, TODO

    return response_dictionary
