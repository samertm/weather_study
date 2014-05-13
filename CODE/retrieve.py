#! /usr/bin/env python
# retrieve.py
# David Prager Branner and Gina Schmalzle
# 20140513, works.

"""Data-retrieval functions for Weather Study project."""

import os
import sys
import sqlite3
import time
import json
import utils as U

def get_multidate_data_from_db(db='weather_data_OWM.db', 
        start_date=None, end_date=None, exact_date=None, to_print=True):
    """Retrieve forecasts for multiple dates, return as list of tuples."""
    # This function is no longer in active use but is left here as a record.
    # We are now (20140513) using mainly `get_single_date_data_from_db()`.
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
            to_print=True, output='dict of tuples', none_values=False):
    """Retrieve forecasts for single date; none_values adds dict of problems."""
    allowed_outputs = ['dict', 'dict of tuples', 'JSON', 'GeoJSON']
    if output not in allowed_outputs:
        print('Argument `output={}` not supported; choose from {}. Exiting.'.
                format(output, allowed_outputs))
        sys.exit(0)
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
    # For readability, we have moved the composition of `composed_data`
    # and `none_values_found` into separate functions.
    if none_values:
        none_values_found = generate_none_values(retrieved_data)
    if output == 'dict of tuples':
        composed_data = generate_dict_of_tuples(retrieved_data)
    elif output == 'JSON':
        composed_data = generate_JSON(retrieved_data)
    else: # output == 'GeoJSON'
        composed_data = generate_GeoJSON(retrieved_data)
    end_time = time.time()
    if to_print:
        print('Total time elapsed: {} seconds'.
                format(round(end_time-start_time)))
    # Prepare return-data — either single item or tuple.
    if output in ('JSON', 'GeoJSON'):
        to_return = json.dumps(composed_data)
    else:
        to_return = composed_data
    if none_values:
        to_return = (to_return, none_values_found)
    return to_return

def generate_none_values(retrieved_data):
    """Compose dictionary telling where `None` is found in data."""
    none_values_found = {
            'None among one whole lat_lon pair': None in [i[0:2] 
                    for i in retrieved_data],
            'None in either lat or lon alone': None in 
                    [subelem for elem in retrieved_data 
                        for subelem in elem[0:2]
                    ],
            'None as one whole forecast': (None, None, None, None) in 
                    [subtuple for tupl in retrieved_data 
                        for subtuple in zip(
                            tupl[2::4], tupl[3::4], tupl[4::4], tupl[5::4]
                        )
                    ],
            }
    none_values_found['None within forecast but not as whole forecast'] = (
            None in 
                [subtuple for tupl in retrieved_data for subtuple in tupl] 
                and not none_values_found['None as one whole forecast'])
    return none_values_found
    # The following was prepared for use with dict-of-tuple output; instead, 
    # however, we are using `none_values_found` dictionary prepared from the
    # database output.
    #    none_values_found = {
    #            'None among tuples': None in [tupl for lst in x.values() 
    #                    for tupl in lst],
    #            'None in tuple-elements': None in [elem for lst in x.values() 
    #                    for tupl in lst 
    #                            if tupl 
    #                        for elem in tupl],
    #            'None in lat_lon pairs': None in [lst for lst in x.keys()],
    #            'None in lat or lon': None in [tupl for lst in x.keys() 
    #                    for tupl in lst],
    #            }

def generate_dict_of_tuples(retrieved_data):
    """Compose the data into a succinct dictionary of tuples."""
    # Our re-composed data type is a dictionary of tuples. 
    # Each tuple contains three items:
    #     sub-tuple containing latitude and longitude (floats);
    #     list of 15 sub-sub-tuples, each containing
    #         maxt, mint, rain, snow (floats).
    # For dates where the database contains no data, the forecast tuple
    # would be: `(None, None, None, None)` but this is replaced by `None`, 
    # using and `if-else` clause.
    composed_data = {}
    for item in retrieved_data:
        lat_lon = item[0:2]
        forecasts = [subitem
                    if subitem[0] or subitem[1] or subitem[2] or subitem[3]
                    else None
                for subitem in 
                zip(item[2::4], item[3::4], item[4::4], item[5::4])]
        composed_data[lat_lon] = forecasts
    return composed_data

def generate_JSON(retrieved_data):
    """Compose the data into a succinct nested dictionary."""
    # Our re-composed data type is a nested dictionary. 
    # Each key-object pair consists of:
    #     key: latitude-longitude pair, string delimited by '_';
    #     value: subdictionary; 
    #         each subdictionary consists of fifteen key-value pairs:
    #         key: integer between 0 and 14, i.e. days before target date;
    #         value: sub-subdictionary;
    #              each sub-subdictionary consists of four key-value pairs:
    #              key: one of 'maxt', 'mint', 'rain', 'snow';
    #              value: a floating point number, 2-place decimal accuracy.
    # Finally, the subdictionary is converted to a JSON string.
    # Where the database contains no data, the sub-subdictionary value
    # would be: `{'mint': None, 'rain': None, 'maxt': None, 'snow': None}`.
    # But we replace that with None alone, using an `if-else` clause.
    composed_data = {
            str(item[0]) + '_' + str(item[1]): {
                i: {
                    'maxt': subitem[0], 'mint': subitem[2],
                    'rain': subitem[2], 'snow': subitem[3]} 
                        if (subitem[0] or subitem[1] or 
                            subitem[2] or subitem[3])
                        else None
                for i, subitem in enumerate(zip(
                            item[2::4], item[3::4], 
                            item[4::4], item[5::4]))}
            for item in retrieved_data}
    return composed_data

def generate_GeoJSON(retrieved_data):
    """Compose the data into the verbose GeoJSON format."""
    # See http://geojson.org/geojson-spec.html.
    composed_data = {
            'type': 'FeatureCollection',
            'features': [
                    {'type': 'Feature',
                    'geometry': {
                            'type': 'Point',
                            'coordinates': [item[0], item[1]],
                            },
                    'properties': {
                            'maxt_0': item[2], 'mint_0': item[3],
                            'rain_0': item[4], 'snow_0': item[5],
                            'maxt_1': item[6], 'mint_1': item[7],
                            'rain_1': item[8], 'snow_1': item[9],
                            'maxt_2': item[10], 'mint_2': item[11],
                            'rain_2': item[12], 'snow_2': item[13],
                            'maxt_3': item[14], 'mint_3': item[15],
                            'rain_3': item[16], 'snow_3': item[17],
                            'maxt_4': item[18], 'mint_4': item[19],
                            'rain_4': item[20], 'snow_4': item[21],
                            'maxt_5': item[22], 'mint_5': item[23],
                            'rain_5': item[24], 'snow_5': item[25],
                            'maxt_6': item[26], 'mint_6': item[27],
                            'rain_6': item[28], 'snow_6': item[29],
                            'maxt_7': item[30], 'mint_7': item[31],
                            'rain_7': item[32], 'snow_7': item[33],
                            'maxt_8': item[34], 'mint_8': item[35],
                            'rain_8': item[36], 'snow_8': item[37],
                            'maxt_9': item[38], 'mint_9': item[39],
                            'rain_9': item[40], 'snow_9': item[41],
                            'maxt_10': item[42], 'mint_10': item[43],
                            'rain_10': item[44], 'snow_10': item[45],
                            'maxt_11': item[46], 'mint_11': item[47],
                            'rain_11': item[48], 'snow_11': item[49],
                            'maxt_12': item[50], 'mint_12': item[51],
                            'rain_12': item[52], 'snow_12': item[53],
                            'maxt_13': item[54], 'mint_13': item[55],
                            'rain_13': item[56], 'snow_13': item[57],
                            'maxt_14': item[58], 'mint_14': item[59],
                            'rain_14': item[60], 'snow_14': item[61],
                            },
            } for item in retrieved_data]
    }
    return composed_data
