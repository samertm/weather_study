#! /usr/bin/python
# utils.py
# David Prager Branner and Gina Schmalzle
# 20140420, works

"""Utilities for Weather Study project."""

import os
import sys
import urllib
import http
import datetime
import time
import json
import glob
import sqlite3
import ast
import shutil
import tarfile
import pprint
import city_codes as CC

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

def request_NOAA_200_cities():
    url = '''http://www.weather.gov/forecasts/xml/sample_products/browser_interface/ndfdXMLclient.php?citiesLevel=1234&product=time-series&maxt=maxt&mint=mint&qpf=qpf&snow=snow&format=24+hourly&numDays=14'''
    while True:
        forecast = make_urlrequest(url)
        if forecast.msg == 'OK':
            break
    # Forecast is of type http.client.HTTPResponse
    # forecast.readall(): bytes; use `.decode()` for long string
    forecast = forecast.readall().decode()
    # Forecast is dict; key 'list' is a list containing most of the content.
    return forecast

def request_all_NOAA_points():
    start_time = time.time()
    # Get newest file of latitude & longitude values.
    files = open_directory('../DATA/CITY_LISTS/city_list_normalized_')
    with open(files[-1], 'r') as f:
        contents = f.read()
    # Construct list of 'latitude,longitude' strings for US points only.
    list_of_lines = [
            line.split('\t') for line in contents.split('\n')[1:] if 
                line[-2:] == 'US']
    lat_and_long_list = [
            line[2] + ',' + line[3] for line in list_of_lines[:-1]]
    # Construct groups of 200 '+'-delimited pairs each of 'lat' + ',' + 'long'.
    groups_of_200 = [lat_and_long_list[i:i+200] for 
            i in range(0, len(lat_and_long_list), 200)]
    # Make requests in groups of 200 and store results in forecasts_list.
    forecasts_list = []
    download_start_time = construct_date()
    for i, group in enumerate(groups_of_200): # debug
        group = '+'.join(group)
        head = ('''http://www.weather.gov/forecasts/xml/sample_products/'''
                '''browser_interface/ndfdXMLclient.php?'''
                '''product=time-series&product=time-series'''
                '''&maxt=maxt&mint=mint&qpf=qpf&snow=snow&listLatLon=''')
        url = head + group
        while True:
            forecast = make_urlrequest(url)
            if forecast.msg == 'OK':
                # Forecast is of type http.client.HTTPResponse
                # forecast.readall(): bytes; use `.decode()` for long string
                try:
                    forecast = forecast.readall().decode()
                except http.client.IncompleteRead as e:
                    print(e, 'at group', i, group, '\n')
                    continue
                if forecast[-8:-1] == '</dwml>':
                    print('Forecast group {}/{} 200-forecast groups received.'.
                            format(i+1, len(groups_of_200)))
                    break
                else:
                    print('Unexpected file received, ending in:', forecast[-8:])
        forecasts_list.append(forecast)
    download_end_time = construct_date()
    # Store raw material in a single directory with time-range stamp.
    if download_start_time.split('-')[0] == download_end_time.split('-')[0]:
        download_end_time = download_end_time.split('-')[-1]
    timestamp = download_start_time + '_to_' + download_end_time
    dir_name = 'downloads_NOAA_US_' + timestamp
    if not os.path.exists('../DATA/DOWNLOADS/' + dir_name):
        os.makedirs('../DATA/DOWNLOADS/' + dir_name)
    for i, forecast in enumerate(forecasts_list):
        with open(os.path.join(
                '../DATA/DOWNLOADS/' + dir_name+'/', str(i)+'.txt'), 'w') as f:
            f.write(forecast)
    end_time = time.time()
    print('\nTime elapsed: {} seconds.'.
            format(round(end_time-start_time)))
    print('Saved to', dir_name)
    tar_directory(dir_name)

def construct_date(date_and_time=None):
    """Construct a time-and-date string for appending to a filename."""
    if not date_and_time:
        date_and_time = datetime.datetime.today()
    date_and_time = date_and_time.strftime('%Y%m%d-%H%M')
    return date_and_time

def convert_from_unixtime(unixtime):
    """Convert Unix time to human-readable string."""
    return datetime.datetime.fromtimestamp(
            unixtime).strftime('%Y-%m-%d %H:%M')

def open_directory(path):
    """Get list of files in a given directory."""
    file_list = glob.glob(path+'*')
    return file_list

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
        if content_dict == None:
            # This happens occasionally. Ignore silently and continue.
            continue
        forecast_list_received =(content_dict['list'])
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

def full_forecast_download_OWM(country='US', db='weather_data_OWM.db'):
    """Download OWN forecasts for set of locations, save to unique directory."""
    start_time = time.time()
    # Create time-stamped directory, with country-name, for this download.
    dir_name = 'downloads_OWM_' + country + '_' + construct_date()
    print('Saving to directory {}'.format(dir_name))
    if not os.path.exists(os.path.join('../DATA/DOWNLOADS/', dir_name)):
        os.makedirs(os.path.join('../DATA/DOWNLOADS/', dir_name))
    # Download all forecasts.
    code_list = CC.get_city_codes_from_db(country, db)
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
            '../DATA/DOWNLOADS/'+dir_name, code+'.txt'), 'w') as f:
            f.write(content)
    end_time = time.time()
    print('\nTime elapsed: {} seconds.'.
            format(round(end_time-start_time)))

def cities_forecast_download_NOAA():
    """Download NOAA forecasts for 200 cities, save to unique directory."""
    start_time = time.time()
    # Create time-stamped directory for this download.
    dir_name = 'downloads_NOAA_200_cities_' + construct_date()
    print('Saving to directory {}'.format(dir_name))
    if not os.path.exists(os.path.join('../DATA/DOWNLOADS/', dir_name)):
        os.makedirs(os.path.join('../DATA/DOWNLOADS/', dir_name))
    # Download all forecasts.
    content = request_NOAA_200_cities()
    with open(os.path.join(
            '../DATA/DOWNLOADS/' + dir_name, dir_name + '.txt'), 'w') as f:
        f.write(content)
    tar_directory(dir_name)
    end_time = time.time()
    print('\nTime elapsed: {} seconds.'.
            format(round(end_time-start_time)))

def tar_directory(dirname=None):
    """Compress all directories found in DOWNLOAD/ and delete originals."""
    start_time = time.time()
    home_dir = os.getcwd()
    os.chdir('../DATA/DOWNLOADS')
    # Do the whole procedure below for any existing directories in DOWNLOADS.
    # First find the directories.
    if not dirname:
        directories = open_directory('downloads_')
    else:
        directories = [dirname]
    print('{} directories to be compressed.'.
            format(len(directories)), end='\n\n')
    # Make sure ../COMPRESSED exists or create it.
    if not os.path.exists('../COMPRESSED'):
        os.makedirs('../COMPRESSED')
        print('Created directory COMPRESSED', end='\n\n')
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
