from deephaven import DynamicTableWriter
import deephaven.dtypes as dht

import json

def extract_sport_radar_json(d, response_dictionary=None, parent_keys=None):
    """
    Extracts data from a SportRadar API JSON response into Deephaven tables

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
            extract_sport_radar_json(d[key], response_dictionary, parent_keys + [key])

        #If list, create a new table
        elif isinstance(d[key], list):
            is_primitives = True
            dtw_columns = {}
            #If the items in the list are dictionaries, add columns to write
            #Since the API doesn't include nulls, we have to loop through all of the items
            #to get the proper schema
            if isinstance(d[key][0], dict):
                is_primitives = False
                for i in range(len(d[key])):
                    for list_key in d[key][i].keys():
                        dtw_columns[list_key] = dht.string #potential TODO: Write other types?
            else:
                dtw_columns = {
                    "Value": dht.string
                }
            dtw = DynamicTableWriter(dtw_columns)

            rd_key = "_".join(parent_keys + [key])
            response_dictionary[rd_key] = dtw
            for list_item in d[key]:
                if is_primitives:
                    row_to_write = [json.dumps(list_item)]
                else:
                    row_to_write = []
                    for list_key in dtw_columns.keys(): #Python 3.7: Dicts are ordered, so this will match the DTW columns
                        if list_key in list_item: #Sanity check in case schemas differ
                            row_to_write.append(str(list_item[list_key]))
                        else:
                            row_to_write.append("")
                dtw.write_row(row_to_write)

        #If primitive, append it to the meta table
        else:
            meta_key = "_".join(parent_keys + [key])
            response_dictionary["meta"].write_row((meta_key, json.dumps(d[key])))

    return response_dictionary
