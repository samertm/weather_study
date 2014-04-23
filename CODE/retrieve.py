#! /usr/bin/python
# retrieve.py
# David Prager Branner and Gina Schmalzle
# 20140423

"""Data-retrieval functions for Weather Study project."""

import os
import sqlite3
import ast
import time
import utils as U
import city_codes as CC

def get_weather_data_from_db(db='weather_data_OWM.db'):
    """Retrieve weather data from database and process."""
    # QQQ We would like to be able to restrict the start and stop dates.
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
            '''FROM locations,owm_values '''
            '''ON owm_values.location_id=locations.id;'''
            )
        except:
            pass
    cursor_output = cursor_output.fetchall()
    # Convert to usable form. We get list of tuples.
    # In each tuple, elements 0, 1 are lat. and lon.; 
    #     the remainder become 4-tuples in a list.
    end_time = time.time()
    print('Total time elapsed: {} seconds'.
            format(round(end_time-start_time)))
    return cursor_output
