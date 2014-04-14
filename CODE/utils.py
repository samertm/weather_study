#! /usr/bin/python
# David Prager Branner
# 20140413

"""Utilities for Weather Study project."""

import os
import urllib
import datetime

def get_api_key(site='owm'):
    if site == 'owm':
        filename = 'owm_api.ignore'
    elif site == 'wu':
        filename = 'wu_api.ignore'
    else:
        return
    with open(os.path.join('../DATA', filename), 'r') as f:
        api_key = f.read()
    print('Obtained API key: {}.'.format(api_key))
    return api_key

# The following is not yet working.
def construct_OWN_api_req(city='2643743,6058560'):
    head = 'http://api.openweathermap.org/data/2.5/find?q=London&units=metric&mode=xml'

# The following is not working yet.
#def construct_WU_api_req(city='New_York', history=None):
#    head = 'http://api.wunderground.com/api/'
#    tail = '/geolookup/conditions/q/'
#    if city:
#        city += '.json'

def get_city_code_list():
    cities = ''
    while cities == '':
        try:
            cities = urllib.request.urlopen(
                    'http://openweathermap.org/help/city_list.txt')
        except urllib.error.URLError as e:
            print(e)
            cities = ''
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
        city_list_filename = 'city_list_bytes_' + construct_date() + '.txt'
        with open(os.path.join('../DATA', city_list_filename), 'wb') as f:
            f.write(cities)
        with open(os.path.join('../DATA', 'hash_of_last.txt'), 'w') as f:
            f.write(str(hash(cities)))
        print('New city-code byte-data saved.')
        # Check for non-ASCII content and normalize.
        chars = set([i for i in cities])
        for c in chars:
            if c > 122:
                print('Non-ASCII character {} ({}) at position {}.'.
                        format(c, repr(chr(c)), cities.find(c)))
        city_list_filename = 'city_list_normalized_' + construct_date() + '.txt'
        normalized = ''.join([chr(char) for char in cities])
        # Here we replace any non-ASCII characters we have found above.
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
