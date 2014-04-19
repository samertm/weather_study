#! /usr/bin/python
# populate_db.py
# David Prager Branner and Gina Schmalzle
# 20140419

"""Database populating tools for weather study."""

import os
import sys
import urllib
import datetime
import time
import json
import glob
import sqlite3
import ast
import shutil
import tarfile
import pprint
import utils as U

def populate_db_w_forecasts(forecast_dict):
    """Populate database with the contents of a forecast dictionary."""
    pass

def process_dir_of_downloads(to_print=None):
    """Populate database with the forecasts from all files in DOWNLOADS."""
    # Get names of directories in download folder
    directories = open_directory('../DOWNLOADS/downloads_OWM_US_')
    # For each directory, get all files
    for directory in directories:
        print(directory) # debug
        files = U.open_directory(directory+'/')
        forecast_dict = U.retrieve_data_vals(files, to_print)
        populate_db_w_forecasts(forecast_dict)

def populate_db_w_city_codes(db='weather_data_OWM.db'):
    """Populate database with contents of most recently saved city code list."""
    connection = sqlite3.connect(os.path.join('../', db))
    with connection:
        cursor = connection.cursor()
        city_codes = U.isolate_city_codes()
        for code in city_codes[1:-1]:
            if code == ['']:
                print('\n    Empty tuple found; skipping.\n')
                continue
            print(str(tuple(code)))
            cursor.execute(
                    '''INSERT INTO locations VALUES''' +
                    str(tuple(code)))
            