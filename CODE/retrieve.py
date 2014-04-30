#! /usr/bin/env python
# retrieve.py
# David Prager Branner and Gina Schmalzle
# 20140430, works.

"""Data-retrieval functions for Weather Study project."""

import os
import sqlite3
import time
import json
import utils as U

def get_multidate_data_from_db(db='weather_data_OWM.db', 
        start_date=None, end_date=None, exact_date=None, to_print=True):
    """Retrieve forecasts for multiple dates, return as list of tuples."""
    start_time = time.time()
    select_string = (
        '''SELECT lat, lon, target_date, '''
        '''maxt_0, mint_0, rain_0, snow_0, '''
        '''maxt_1, mint_1, rain_1, snow_1, '''
        '''maxt_2, mint_2, rain_2, snow_2, '''
        '''maxt_3, mint_3, rain_3, snow_3, '''
        '''maxt_4, mint_4, rain_4, snow_4, '''
        '''maxt_5, mint_5, rain_5, snow_5, '''
        '''maxt_6, mint_6, rain_6, snow_6, '''
        '''maxt_7, mint_7, rain_7, snow_7, '''
        '''maxt_8, mint_8, rain_8, snow_8, '''
        '''maxt_9, mint_9, rain_9, snow_9, '''
        '''maxt_10, mint_10, rain_10, snow_10, '''
        '''maxt_11, mint_11, rain_11, snow_11, '''
        '''maxt_12, mint_12, rain_12, snow_12, '''
        '''maxt_13, mint_13, rain_13, snow_13, '''
        '''maxt_14, mint_14, rain_14, snow_14 '''
        '''FROM locations, owm_values '''
        '''ON owm_values.location_id=locations.id;''')
    # If dates are specified, we need an addition tuple "dates" for `execute`.
    if exact_date:
        # Add condition to end of select_string. 
        # We ignore start_date and end_date in this case.
        select_string = select_string.replace(';', ' WHERE target_date=?;')
        dates = (exact_date, )
    elif start_date and end_date:
        # Add condition to end of select_string
        select_string = select_string.replace(
                ';', ' WHERE target_date>=? AND target_date<=?;')
        dates = (start_date, end_date)
    elif start_date and not end_date:
        # Add condition to end of select_string
        select_string = select_string.replace(';', ' WHERE target_date>=?;')
        dates = (start_date,)
    elif end_date and not start_date:
        # Add condition to end of select_string
        select_string = select_string.replace(';', ' WHERE target_date<=?;')
        dates = (end_date,)
    connection = sqlite3.connect(os.path.join('../', db))
    with connection:
        cursor = connection.cursor()
        try:
            if exact_date or start_date or end_date:
                cursor_output = cursor.execute(select_string, dates)
            else:
                cursor_output = cursor.execute(select_string)
        except Exception as e:
            # What exceptions may we encounter here?
            print(e)
    # Convert to usable form. We receive list of simple tuples from database.
    retrieved_data = cursor_output.fetchall()
    # Our re-composed data type is a list of tuples. 
    # Each tuple contains three items:
    #     sub-tuple containing latitude and longitude (floats);
    #     target_date (int);
    #     list of 15 sub-sub-tuples, each containing
    #         maxt, mint, rain, snow (floats).
    # For dates where the database contains no data, the forecast tuple
    # is: `(None, None, None, None)`.
    composed_data = []
    for item in retrieved_data:
        lat_lon = item[0:2]
        target_date = item[2]
        forecasts = [subitem for subitem in 
                zip(item[3::4], item[4::4], item[5::4], item[6::4])]
        composed_data.append((lat_lon, target_date, forecasts))
    # In each tuple, elements 0, 1 are lat. and lon.; 
    #     the remainder become 4-tuples in a list.
    end_time = time.time()
    if to_print:
        print('Total time elapsed: {} seconds'.
                format(round(end_time-start_time)))
    return composed_data

def get_single_date_data_from_db(exact_date, db='weather_data_OWM.db',
            to_print=True):
    """Retrieve forecasts for single date, return as dictionary."""
    start_time = time.time()
    connection = sqlite3.connect(os.path.join('../', db))
    with connection:
        cursor = connection.cursor()
        try:
            cursor_output = cursor.execute(
                '''SELECT lat, lon, '''
                '''maxt_0, mint_0, rain_0, snow_0, '''
                '''maxt_1, mint_1, rain_1, snow_1, '''
                '''maxt_2, mint_2, rain_2, snow_2, '''
                '''maxt_3, mint_3, rain_3, snow_3, '''
                '''maxt_4, mint_4, rain_4, snow_4, '''
                '''maxt_5, mint_5, rain_5, snow_5, '''
                '''maxt_6, mint_6, rain_6, snow_6, '''
                '''maxt_7, mint_7, rain_7, snow_7, '''
                '''maxt_8, mint_8, rain_8, snow_8, '''
                '''maxt_9, mint_9, rain_9, snow_9, '''
                '''maxt_10, mint_10, rain_10, snow_10, '''
                '''maxt_11, mint_11, rain_11, snow_11, '''
                '''maxt_12, mint_12, rain_12, snow_12, '''
                '''maxt_13, mint_13, rain_13, snow_13, '''
                '''maxt_14, mint_14, rain_14, snow_14 '''
                '''FROM locations, owm_values '''
                '''ON owm_values.location_id=locations.id '''
                '''WHERE target_date=?''', (exact_date,))
        except Exception as e:
            # What exceptions may we encounter here?
            print(e)
    # Convert to usable form. We receive list of simple tuples from database.
    retrieved_data = cursor_output.fetchall()
    # Our re-composed data type is a dictionary. 
    # Each tuple contains three items:
    #     sub-tuple containing latitude and longitude (floats);
    #     list of 15 sub-sub-tuples, each containing
    #         maxt, mint, rain, snow (floats).
    # For dates where the database contains no data, the forecast tuple
    # is: `(None, None, None, None)`.
    composed_data = {}
    for item in retrieved_data:
        lat_lon = item[0:2]
        forecasts = [subitem for subitem in 
                zip(item[2::4], item[3::4], item[4::4], item[5::4])]
        composed_data[lat_lon] = forecasts
    # In each tuple, elements 0, 1 are lat. and lon.; 
    #     the remainder become 4-tuples in a list.
    end_time = time.time()
    if to_print:
        print('Total time elapsed: {} seconds'.
                format(round(end_time-start_time)))
    return composed_data

def get_single_date_data_from_db_json(exact_date, db='weather_data_OWM.db',
            to_print=True, JSONize=True):
    """Retrieve forecasts for single date, return as JSON nested dictionary."""
    start_time = time.time()
    connection = sqlite3.connect(os.path.join('../', db))
    with connection:
        cursor = connection.cursor()
        try:
            cursor_output = cursor.execute(
                '''SELECT lat, lon, '''
                '''maxt_0, mint_0, rain_0, snow_0, '''
                '''maxt_1, mint_1, rain_1, snow_1, '''
                '''maxt_2, mint_2, rain_2, snow_2, '''
                '''maxt_3, mint_3, rain_3, snow_3, '''
                '''maxt_4, mint_4, rain_4, snow_4, '''
                '''maxt_5, mint_5, rain_5, snow_5, '''
                '''maxt_6, mint_6, rain_6, snow_6, '''
                '''maxt_7, mint_7, rain_7, snow_7, '''
                '''maxt_8, mint_8, rain_8, snow_8, '''
                '''maxt_9, mint_9, rain_9, snow_9, '''
                '''maxt_10, mint_10, rain_10, snow_10, '''
                '''maxt_11, mint_11, rain_11, snow_11, '''
                '''maxt_12, mint_12, rain_12, snow_12, '''
                '''maxt_13, mint_13, rain_13, snow_13, '''
                '''maxt_14, mint_14, rain_14, snow_14 '''
                '''FROM locations, owm_values '''
                '''ON owm_values.location_id=locations.id '''
                '''WHERE target_date=?''', (exact_date,))
        except Exception as e:
            # What exceptions may we encounter here?
            print(e)
    # Convert to usable form. We receive list of simple tuples from database.
    retrieved_data = cursor_output.fetchall()
    # Our re-composed data type is a nested dictionary. 
    # Each key-object pair consists of:
    #     key: latitude-longitude pair, string delimited by '_';
    #     value: subdictionary; 
    #         each subdictionary consists of fifteen key-value pairs:
    #         key: integer between 0 and 14, meaning days before target date;
    #         value: sub-subdictionary;
    #              each sub-subdictionary consists of four key-value pairs:
    #              key: one of 'maxt', 'mint', 'rain', 'snow';
    #              value: a floating point number, 2 places' decimal accuracy.
    # Finally, the subdictionary is converted to a JSON string.
    # For dates where the database contains no data, the sub-subdictionary value
    # is: `{'mint': None, 'rain': None, 'maxt': None, 'snow': None}`.
    composed_data = {
            str(item[0]) + '_' + str(item[1]): {
                i: {
                    'maxt': subitem[0], 'mint': subitem[2],
                    'rain': subitem[2], 'snow': subitem[3]} 
                for i, subitem in enumerate(zip(
                            item[2::4], item[3::4], item[4::4], item[5::4]))}
            for item in retrieved_data}
    # In each tuple, elements 0, 1 are lat. and lon.; 
    #     the remainder become 4-tuples in a list.
    end_time = time.time()
    if to_print:
        print('Total time elapsed: {} seconds'.
                format(round(end_time-start_time)))
    if not JSONize:
        return composed_data
    else:
        return json.dumps(composed_data)
