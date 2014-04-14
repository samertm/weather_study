#! /usr/bin/python
# David Prager Branner
# 20140413

"""Utilities for Weather Study project."""

import os
import urllib
import datetime
import json

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
            print(e)
            content = ''
    return content

# The following is not yet fully working.
def construct_OWM_api_req(id='5128581', count=14): # ID 5128581 = New York City
    """Attempt OWM query."""
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
    return forecast
    # forecast is dict; key 'list' is a list containing most of the content.

# The following is not working yet.
#def construct_WU_api_req(city='New_York', history=None):
#    head = 'http://api.wunderground.com/api/'
#    tail = '/geolookup/conditions/q/'
#    if city:
#        city += '.json'

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
