from deephaven import DynamicTableWriter
import deephaven.dtypes as dht
from deephaven.time import to_datetime
from dateutil import parser

import json
import re

def sportradar_datetime_converter(datetime_str):
    match = re.match(r'(\d{4})-(\d{2})-(\d{2})T(\d{2}):(\d{2}):(\d{2})', datetime_str)

    if not bool(match):
        return None

    try:
        dt = parser.parse(datetime_str)
        dts = dt.strftime("%Y-%m-%dT%H:%M:%S") + " UTC"
        return to_datetime(dts)
    except:
        return None

class MissingNullsJsonWriter:
    """
    A class that writes rows to a Deephaven table that handles missing null values in a JSON object.

    Attributes:
        rows (list<dict>): A list of dictionaries representing each row to write
        columns (dict): A dictionary representing the columns to write
        datetime_converter (method): A method that takes a string and converts it
            to a Deephaven DateTime object. If the string isn't convertable to a
            DateTime object, None should be returned
    """

    def __init__(self, datetime_converter=None):
        self.rows = []
        self.columns = {}
        self.datetime_converter = datetime_converter

    def _build_columns(self):
        """
        Builds the columns attribute based on the current rows

        Returns:
            None
        """
        self.columns = {}

        for row in self.rows:
            for column in row:
                if not (column in self.columns):
                    type_ = None
                    #NOTE: The order of these if statements DOES matter. The bool check
                    #needs to come before the int check. Why? Because bool is a subclass of int
                    #https://stackoverflow.com/questions/37888620/comparing-boolean-and-int-using-isinstance
                    if isinstance(row[column], bool):
                        type_ = dht.bool_
                    elif isinstance(row[column], int):
                        type_ = dht.int_
                    elif isinstance(row[column], float):
                        type_ = dht.double
                    #Check if it could be a DateTime
                    elif (self.datetime_converter is not None) and (self.datetime_converter(row[column]) is not None):
                        type_ = dht.DateTime
                    #Default to string
                    else:
                        type_ = dht.string
                    self.columns[column] = type_

    def add_row(self, row_to_add):
        """
        Adds the row to the list of rows to write
        
        Parameters:
            row_to_add (dict): A dictionary representing a single row to write
        Returns:
            None
        """
        self.rows.append(row_to_add)

    def create_table(self):
        """
        Creates the Deephaven table for the given data

        Returns:
            Table: The Deephaven table with the data written to it, handling nulls as empty strings
        """
        self._build_columns()

        dtw = DynamicTableWriter(self.columns)

        for row in self.rows:
            row_to_write = []
            for column in self.columns:
                #Another null check
                if column in row:
                    #Check if DateTime, if so convert to a Deephaven DateTime object
                    if self.columns[column] == dht.DateTime:
                        row_to_write.append(self.datetime_converter(row[column]))
                    else:
                        row_to_write.append(row[column])
                else:
                    row_to_write.append(None)
            dtw.write_row(row_to_write)

        return dtw.table

def flatten_dict(d, key_prefix=None):
    """
    Flattens the given dictionary by changing nested dictionaries into upper level primitives.

    For example:
        {
            "a": {
                "b": "c",
                "d": "e"
            }
        }

    becomes
        {
            "a_b": "c",
            "a_d": "e",
        }

    Parameters:
        d (dict): The dictionary to flatten
        key_prefix (str): The prefix for flattened keys on recursive calls
    Returns:
        dict: The flattened dictionary
    """
    flattened_d = {}
    for key in d:
        if key_prefix is None:
            next_key_prefix = key
        else:
            next_key_prefix = f"{key_prefix}_{key}"

        if isinstance(d[key], dict):
            flattened_d = {**flattened_d, **flatten_dict(d[key], next_key_prefix)}
        else:
            flattened_d[next_key_prefix] = d[key]

    return flattened_d

def extract_sport_radar_json(d, response_dictionary=None, parent_keys=None, table_to_write=None, datetime_converter=sportradar_datetime_converter):
    """
    Extracts data from a SportRadar API JSON response into Deephaven tables

    Parameters:
        d (dict|list): The SportRadar API JSON response as a Python dictionary or list
        response_dictionary (dict): The response_dictionary used to store info for recursive calls
        parent_keys (list<str>): The JSON keys that led to the current dictionary in recursive calls
        table_to_write (str): The key in the response_dictionary to write to
        datetime_converter (method): A method that takes a string and converts it
            to a Deephaven DateTime object. If the string isn't convertable to a
            DateTime object, None should be returned
    Returns:
        dict<str, DynamicTableWriter>: Key value pairs that map to Deephaven table writers
    """
    if response_dictionary is None:
        response_dictionary = {}
    if table_to_write is None:
        table_to_write = "base"
    if parent_keys is None:
        parent_keys = ["base"]

    iter_ = None
    is_list = False
    if isinstance(d, dict):
        d = flatten_dict(d)
        iter_ = d.keys()
    elif isinstance(d, list):
        iter_ = range(len(d))
        is_list = True

    write_values = {}
    for key in iter_:
        #If dictionary, simply recurse with the new key appended to parent_keys
        if isinstance(d[key], dict):
            extract_sport_radar_json(d[key], response_dictionary, parent_keys + [key], table_to_write, datetime_converter)
        #If list, recurse with with the new key appended to parent_keys and a new table to write
        elif isinstance(d[key], list):
            extract_sport_radar_json(d[key], response_dictionary, parent_keys + [key], table_to_write + f"_{str(key)}", datetime_converter)
        #If primitive, write it
        else:
            write_values[key] = d[key]

    if not table_to_write in response_dictionary:
        response_dictionary[table_to_write] = MissingNullsJsonWriter(datetime_converter=datetime_converter)

    if len(write_values) > 0:
        response_dictionary[table_to_write].add_row(write_values)

    return response_dictionary
