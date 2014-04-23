#! /usr/bin/python
# requests.py
# David Prager Branner and Gina Schmalzle
# 20140422, works

"""Data-request (and related) functions for Weather Study project."""

import os
import urllib
import http
import time
import json
import utils as U
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

def construct_OWM_api_request(id='5128581', count=15): 
    # ID 5128581 = New York City
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

def construct_NOAA_request_200_cities():
    """Make request of forecast data from NOAA for 200 Level 1/2/3/4 cities."""
    url = '''http://www.weather.gov/forecasts/xml/sample_products/browser_interface/ndfdXMLclient.php?citiesLevel=1234&product=time-series&maxt=maxt&mint=mint&qpf=qpf&snow=snow&format=24+hourly&Unit=m'''
    while True:
        forecast = make_urlrequest(url)
        if forecast.msg == 'OK':
            break
    # Forecast is of type http.client.HTTPResponse
    # forecast.readall(): bytes; use `.decode()` for long string
    forecast = forecast.readall().decode()
    # Forecast is dict; key 'list' is a list containing most of the content.
    return forecast

def download_NOAA_all_US_points(limit=None):
    """Make request of forecast data from NOAA for all the US cities at OWM."""
    start_time = time.time()
    # Get newest file of latitude & longitude values.
    files = U.open_directory('../DATA/CITY_LISTS/city_list_normalized_')
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
    download_start_time = U.construct_date()
    for i, group in enumerate(groups_of_200): # debug
        # Truncate if there is a limit.
        if i == limit:
            break
        group = '+'.join(group)
        head = ('''http://www.weather.gov/forecasts/xml/sample_products/'''
                '''browser_interface/ndfdXMLclient.php?'''
                '''product=time-series&product=time-series&format=24+hourly'''
                '''&Unit=m&maxt=maxt&mint=mint&qpf=qpf&snow=snow&listLatLon=''')
        url = head + group
        while True:
            forecast = make_urlrequest(url)
            if forecast.msg == 'OK':
                # Forecast is of type http.client.HTTPResponse
                # forecast.readall(): bytes; use `.decode()` for long string
                try:
                    forecast = forecast.readall().decode()
                except http.client.IncompleteRead as e:
                    print(e, 'at group', i+1)
                    continue
                if forecast[-8:-1] == '</dwml>':
                    print('Forecast group {}/{} 200-forecast groups received.'.
                            format(i+1, len(groups_of_200)))
                    break
                else:
                    print('Unexpected file received, ending in:', forecast[-8:])
        forecasts_list.append(forecast)
    download_end_time = U.construct_date()
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
    U.tar_directory(dir_name)

def download_OWM_full_forecast(country='US', db='weather_data_OWM.db', 
            limit=None):
    """Download OWN forecasts for set of locations, save to unique directory."""
    start_time = time.time()
    # Create time-stamped directory, with country-name, for this download.
    dir_name = 'downloads_OWM_' + country + '_' + U.construct_date()
    print('Saving to directory {}'.format(dir_name))
    if not os.path.exists(os.path.join('../DATA/DOWNLOADS/', dir_name)):
        os.makedirs(os.path.join('../DATA/DOWNLOADS/', dir_name))
    # Download all forecasts.
    code_list = CC.get_city_codes_from_db(country, db)
    for i, code in enumerate(code_list):
        # Truncate if there is a limit.
        if i == limit:
            break
        # Print stats so we can see where we are in long download.
        if not i % 100:
            length = len(code_list)
            print('{:>6d} done out of {}: {}%.'.
                    format(i, length, round(i*100/length, 1)))
        content = str(construct_OWM_api_request(id=code))
        if content == 'None':
            print('Received "None" reply on query for city {}.'.format(code))
            continue
        with open(os.path.join(
            '../DATA/DOWNLOADS/'+dir_name, code+'.txt'), 'w') as f:
            f.write(content)
    U.tar_directory(dir_name)
    end_time = time.time()
    print('\nTime elapsed: {} seconds.'.
            format(round(end_time-start_time)))

def download_NOAA_cities_forecast():
    """Download NOAA forecasts for 200 cities, save to unique directory."""
    start_time = time.time()
    # Create time-stamped directory for this download.
    dir_name = 'downloads_NOAA_200_cities_' + U.construct_date()
    print('Saving to directory {}'.format(dir_name))
    if not os.path.exists(os.path.join('../DATA/DOWNLOADS/', dir_name)):
        os.makedirs(os.path.join('../DATA/DOWNLOADS/', dir_name))
    # Download all forecasts.
    content = construct_NOAA_request_200_cities()
    with open(os.path.join(
            '../DATA/DOWNLOADS/' + dir_name, dir_name + '.txt'), 'w') as f:
        f.write(content)
    U.tar_directory(dir_name)
    end_time = time.time()
    print('\nTime elapsed: {} seconds.'.
            format(round(end_time-start_time)))

