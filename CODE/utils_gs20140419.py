#! /usr/bin/python
# utils.py
# David Prager Branner and Gina Schmalzle
# 20140417, works

"""Utilities for Weather Study project."""

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

def get_api_key(site='owm', show=False):
    """Without allowing API key to appear in repo, fetch from file."""
    if site == 'owm':
        filename = 'owm_api.ignore'
    elif site == 'wu':
        filename = 'wu_api.ignore'
    else:
        return
    with open(os.path.join('../DATA', filename), 'r') as f:
        api_key = f.read()
    if show:
        print('Obtained API key: {}'.format(api_key))
    return api_key

def make_urlrequest(url):
    """Tries to make URL request until successful."""
    content = ''
    while content == '':
        try:
            content = urllib.request.urlopen(url)
        except urllib.error.URLError as e:
            print(url, e, sep='\n', end='\n\n')
            content = ''
    return content

def construct_OWM_api_req(id='5128581', count=15): # ID 5128581 = New York City
    """Make OWM forecast query."""
    # "...daily..." required for the `count` variable to be meaningful.
    head = 'http://openweathermap.org/data/2.5/forecast/daily?'
    id_string = 'id=' + id
    count_string = '&cnt=' + str(count)
    units = '&units=metric'
    mode = '&mode=daily_compact' # Not clear how this affects, but does affect.
    the_type = '&type=day'
    appid = '&APPID=' + get_api_key() # Apparently goes last or empty results.
    url = head + id_string + units + count_string + mode + the_type + appid
    while True:
        forecast = make_urlrequest(url)
        if forecast.msg == 'OK':
            break
    # Forecast is of type http.client.HTTPResponse
    # forecast.readall(): bytes; use `.decode()` for long string
    forecast = forecast.readall().decode()
    forecast = json.loads(forecast)
    # Forecast is dict; key 'list' is a list containing most of the content.
    return forecast

def get_city_code_list():
    """Get city code list from OWM; check to see if changed; save; normalize."""
    cities = make_urlrequest( 'http://openweathermap.org/help/city_list.txt')
    # Is content changed?
    # Compare hash to hash of previously downloaded version.
    cities = cities.read()
    hash_of_last = ''
    try:
        with open(os.path.join('../DATA', 'hash_of_last.txt'), 'r') as f:
            hash_of_last = f.read()
    except IOError as e:
        print(e)
        print('Continuing.')
        hash_of_last = '0'
    except Exception as e:
        print('Unexpected error:', e)
    if hash(cities) != int(hash_of_last):
        print('hash of new: {}\nlast saved hash: {}'.
                format(hash(cities), int(hash_of_last)), sep='\n')
        print('City-code byte-data retrieved, proves different from previous.')
        # Why do we need to save bytes version of list, if we also save the
        # normalized string version and a hash of the bytes version?
        city_list_filename = 'city_list_bytes_' + construct_date() + '.txt'
        with open(os.path.join('../DATA', city_list_filename), 'wb') as f:
            f.write(cities)
        # Save new hash of current version.
        with open(os.path.join('../DATA', 'hash_of_last.txt'), 'w') as f:
            f.write(str(hash(cities)))
        # Report any non-ASCII content to STDOUT and normalize.
        chars = set([i for i in cities])
        for c in chars:
            if c > 122:
                print('Non-ASCII character {} ({}) at position {}.'.
                        format(c, repr(chr(c)), cities.find(c)))
        city_list_filename = 'city_list_normalized_' + construct_date() + '.txt'
        normalized = ''.join([chr(char) for char in cities])
        # Here we replace any non-ASCII characters we know about already.
        normalized = normalized.replace(chr(150), '-')
        with open(os.path.join('../DATA', city_list_filename), 'w') as f:
            f.write(normalized)
        print('Normalized city-code data saved.')
    else:
        print('No change in data found.')

def construct_date():
    """Construct a time-and-date string for appending to a filename."""
    time = datetime.datetime.today()
    time = time.strftime('%Y%m%d-%H%M')
    return time

def convert_from_unixtime(unixtime):
    """Convert Unix time to human-readable string."""
    return datetime.datetime.fromtimestamp(
            unixtime).strftime('%Y-%m-%d %H:%M')

def open_last_city_list():
    """Find filename of most recently saved city code list."""
    file_list = glob.glob('../DATA/city_list*')
    filename = file_list[-1]
    return filename.split('/')[-1]

def open_directory(path):
    """Get list of files in a given directory."""
    file_list = glob.glob(path+'*')
    return file_list

def process_dir_of_downloads():
    """Populate database with the forecasts from all files in DOWNLOADS."""
    # Get names of directories in download folder
    directories = open_directory('../DOWNLOADS/downloads_OWM_US_')
    # For each directory, get all files
    for directory in directories:
        print(directory) # debug
        files = open_directory(directory+'/')
        forecast_dict = retrieve_data_vals(files)
        populate_db_w_forecasts(forecast_dict)

def populate_db_w_forecasts(forecast_dict, db='weather_data_OWM.db'):
    """Populate database with the contents of a forecast dictionary."""
    connection = sqlite3.connect(os.path.join('../', db))
    with connection:
        cursor = connection.cursor()
        fc = forecast_dict['city_id']
        for code in city_codes[1:-1]:
            if code == ['']:
                print('\n    Empty tuple found; skipping.\n')
                continue
            print(str(tuple(code)))
            cursor.execute(
                    '''INSERT INTO locations VALUES''' +
                    str(tuple(code)))

def retrieve_data_vals(files, to_print=None):
    """From a list of files return a dictionary of forecasts.

    Dictionary contains:

      * query_date (from directory name in filenames) and
      * a series of "city_id:forecast_list_pruned" pairs.

    Each "forecast_list_pruned" list contains tuples, bearing:

      * target date/time,
      * max temp.,
      * min. temp., and
      * rain,
      * snow.
    """
    # Get the date of the query from the filename. `dt` values vary too much.
    filename = files[0]
    dir_name = filename.split('/')[-2] # e.g. downloads_OWM_US_20140414-2215
    query_date = dir_name.split('_')[-1] # e.g. 20140414-2215
    # Process each file
    forecast_dict = {'query_date': query_date}
    for file in files:
        forecast_list_pruned = []
        with open(os.path.join(file), 'r') as f:
            contents = f.read()
        content_dict = ast.literal_eval(contents)
        forecast_list_received =(content_dict['list'])
        if content_dict == 'None':
            # This happens occasionally. Ignore silently and continue.
            continue
        city_id = (content_dict['city']['id'])
        for i, forecast in enumerate(forecast_list_received):
            if 'rain' in forecast:
               rain = forecast['rain']
            else:
               # We believe that when 'rain' is forecast to be zero, no 'rain'
               # key is placed in the forecast.
               rain = 0
            if 'snow' in forecast:
                # We have found explicit examples of snow = 0; not same
                # situation as rain.
                snow = forecast['snow']
            else:
                snow = 0
            forecast_tuple = (
                    forecast['dt'],
                    float(forecast['temp']['max']),
                    float(forecast['temp']['min']),
                    float(rain),
                    float(snow),
                    )
            forecast_list_pruned.append(forecast_tuple)
        forecast_dict[city_id] = forecast_list_pruned
    if to_print:
        pprint.pprint(forecast_dict) # debug
        print('\n') # debug
    return forecast_dict

def isolate_city_codes():
    """Get contents of most recently saved city code list, as list of lists."""
    filename = open_last_city_list()
    with open(os.path.join('../DATA', filename), 'r') as f:
        contents = f.read()
    list_of_lines = [line.split('\t') for line in contents.split('\n')[1:]]
    # Latitude and longitude should be numbers
    for i in range(1, len(list_of_lines)-1):
        list_of_lines[i][2] = float(list_of_lines[i][2])
        list_of_lines[i][3] = float(list_of_lines[i][3])
    print('Total number of city codes: {}.'.format(len(list_of_lines)))
    return list_of_lines

def populate_db_w_city_codes(db='weather_data_OWM.db'):
    """Populate database with contents of most recently saved city code list."""
    connection = sqlite3.connect(os.path.join('../', db))
    with connection:
        cursor = connection.cursor()
        city_codes = isolate_city_codes()
        for code in city_codes[1:-1]:
            if code == ['']:
                print('\n    Empty tuple found; skipping.\n')
                continue
            print(str(tuple(code)))
            cursor.execute(
                    '''INSERT INTO locations VALUES''' +
                    str(tuple(code)))

def get_city_codes_from_db(country='US', db='weather_data_OWM.db'):
    """Get city codes only from database and return as list."""
    connection = sqlite3.connect(os.path.join('../', db))
    with connection:
        cursor = connection.cursor()
        if country:
            id_hits = cursor.execute(
                    '''SELECT id FROM locations WHERE country=?''', (country,))
        else:
            id_hits = cursor.execute(
                    '''SELECT id FROM locations''')
        if id_hits:
            try:
                id_hits = id_hits.fetchall()
            except sqlite3.IntegrityError or IndexError as e:
                print('\n    ', e)
    # id_hits is now a list of 1-tuples. Convert to plain list and retur.
    return [i[0] for i in id_hits]

def full_forecast_download(country='US', db='weather_data_OWM.db'):
    """Download forecasts for set of locations and save to unique directory."""
    start_time = time.time()
    # Create time-stamped directory, with country-name, for this download.
    dir_name = 'downloads_OWM_' + country + '_' + construct_date()
    print('Saving to directory {}'.format(dir_name))
    if not os.path.exists(os.path.join('../DOWNLOADS/', dir_name)):
        os.makedirs(os.path.join('../DOWNLOADS/', dir_name))
    # Download all forecasts.
    code_list = get_city_codes_from_db(country, db)
    for i, code in enumerate(code_list):
        # Print stats so we can see where we are in long download.
        if not i % 100:
            length = len(code_list)
            print('{:>6d} done out of {}: {}%.'.
                    format(i, length, round(i*100/length, 1)))
        content = str(construct_OWM_api_req(id=code))
        if content == 'None':
            print('Received "None" reply on query for city {}.'.format(code))
            continue
        with open(os.path.join(
            '../DOWNLOADS/'+dir_name, code+'.txt'), 'w') as f:
            f.write(content)
    end_time = time.time()
    print('\nTime elapsed: {} seconds.'.
            format(round(end_time-start_time)))

def tar_directory():
    """Compress all directories found in DOWNLOAD/ and delete originals."""
    start_time = time.time()
    home_dir = os.getcwd()
    os.chdir('../DOWNLOADS')
    # Do the whole procedure below for any existing directories in DOWNLOADS.
    # First find the directories.
    directories = open_directory('downloads_OWM_US_')
    print('{} directories to be compressed.'.
            format(len(directories)), end='\n\n')
    # Make sure ../COMPRESSED exists or create it.
    if not os.path.exists('../COMPRESSED'):
        os.makedirs('../COMPRESSED')
        print('Created directory ../COMPRESSED', end='\n\n')
    # Now compress each directory and finally delete it.
    for directory in directories:
        file_list = glob.glob(directory+'/*')
        print('{} files to compress in directory\n    "{}":'.
                format(len(file_list), directory))
        # Compress each contained file, using context manager.
        with tarfile.open(
                '../COMPRESSED/' + directory + '.tar.bz2', 'w:bz2') as f:
            for i, item in enumerate(file_list):
                f.add(item)
                if not i % 1000:
                    length = len(file_list)
                    print('{} files compressed out of {}: {}%.'.
                            format(i, length, round(i*100/length, 1)))
        print('\n{} files compressed in directory\n    "{}".'.
                format(len(file_list), directory), end='\n\n')
        # Once directory is compressed, we would like to delete uncompressed
        # version. `shutil` makes this easier than `os.rmdir` etc.
        shutil.rmtree(directory)
        print('Original directory "{}" deleted.'.format(directory), end='\n\n')
        print('—' * 40, end='\n\n')
    # When finished, return to directory where we started.
    os.chdir(home_dir)
    end_time = time.time()
    total_time = round(end_time - start_time)
    print('Total time elapsed: {} seconds; {} seconds per directory on avg.'.
            format(total_time, round(total_time/len(directories), 1)))