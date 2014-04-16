#! /usr/bin/python
# utils.py
# David Prager Branner
# 20140414, works

"""Utilities for Weather Study project."""

import os
import urllib
import datetime
import time
import json
import glob
import sqlite3
import ast

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
#    cities = ''
#    while cities == '':
#        try:
#            cities = urllib.request.urlopen(
#        except urllib.error.URLError as e:
#            print(e)
#            cities = ''
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
        print('City-code byte-data retrieved, proves different from previous.')
        # Why do we need to save bytes version of list, if we also save the
        # normalized string version and a hash of the bytes version?
#        city_list_filename = 'city_list_bytes_' + construct_date() + '.txt'
#        with open(os.path.join('../DATA', city_list_filename), 'wb') as f:
#            f.write(cities)
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

def open_download_values(path):
    """Find filename of most recently saved values downloads."""
    file_list = glob.glob(path+'*')
    return file_list

# The following function is still under way.
def retrieve_data_vals():
    # Purpose of this function is to create a hash from a hash.  The new hash
    # will have a reduced number of key value pairs that will be used in our
    # data analysis, including dt, min, maxt, rain and city id.
    """ """
    reduced_hash = {}
    # Get names of directories in download folder
    directories = open_download_values('../DOWNLOADS/downloads_OWM_US_')
    # For each directory, get all files
    for directory in directories:
        files = open_download_values(directory+'/')	
            # Process each file
        for file in files[0:1]:
            print(file)
            with open(os.path.join(file), 'r') as f:
               contents = f.read()
            content_dict = ast.literal_eval(contents)
            forecast_list =(content_dict['list'])
            city_id = (content_dict['city']['id'])
            i  = 0
            for forecast in forecast_list:
                if i == 0:
                   target_date = forecast['dt']
                if 'rain' in forecast:
                   rn = forecast['rain']
                   print(city_id,target_date,forecast['dt'], forecast['temp']['max'],forecast['temp']['min'],forecast['rain'])
                else:
                   rn = 'NA'
                   print(city_id,target_date,forecast['dt'], forecast['temp']['max'],forecast['temp']['min'],'NA')
                reduced_hash[i,file] = {'forecast': { 'id' : city_id , 'target_date' : target_date, 'dt' : forecast['dt'], 'tmax' : forecast['temp']['max'], 'tmin' : forecast['temp']['min'], 'rain' : rn }}
                i = i + 1
    return reduced_hash[5,'../DOWNLOADS/downloads_OWM_US_20140415-1628/4046255.txt']
    

def isolate_city_codes():
    """Get contents of most recently saved city code list, as list of lists."""
    filename = open_last_city_list()
    with open(os.path.join('../DATA', filename), 'r') as f:
        contents = f.read()
    return [line.split('\t') for line in contents.split('\n')]

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

def get_city_codes(country='US', db='weather_data_OWM.db'):
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
    code_list = get_city_codes(country, db)
    for i, code in enumerate(code_list):
        # Print stats so we can see where we are in long download.
        if not i % 100:
            print('{:>6d} done out of {}: {:%}.'.
                    format(i, len(code_list), i/len(code_list)))
        content = str(construct_OWM_api_req(id=code))
        with open(os.path.join(
            '../DOWNLOADS/'+dir_name, code+'.txt'), 'w') as f:
            f.write(content)
    end_time = time.time()
    print('\nTime elapsed: {} seconds.'.format(
        round(end_time-start_time)))
