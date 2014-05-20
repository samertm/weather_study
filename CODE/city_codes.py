#! /usr/bin/env python
# city_codes.py
# David Prager Branner and Gina Schmalzle
# 20140519

"""City-code tools for Weather Study project."""

import os
import glob
import sqlite3
import utils as U
import requests as RQ
import hashlib
import logging

def get_city_code_list():
    """Get city code list from OWM; check to see if changed; save; normalize."""
    logger = logging.getLogger('city_codes')
    logger.setLevel(logging.ERROR)
    logging.basicConfig(level=logging.ERROR,
            filename='../logs/weather_study_city_codes.log',
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    url = 'http://openweathermap.org/help/city_list.txt'
    cities = RQ.make_urlrequest(url, logger)
    cities = cities.read()
    # Is content changed?
    #
    # Compare hash to hash of previously downloaded version.
    hash_of_last = ''
    try:
        with open(os.path.join(
                '../DATA/CITY_LISTS', 'hash_of_last.txt'), 'r') as f:
            hash_of_last = f.read()
    except IOError as e:
        print(e)
        print('Continuing.')
        hash_of_last = '0'
    except Exception as e:
        print('Unexpected error:', e)
    md5 = hashlib.md5(cities).hexdigest()
    if md5 != hash_of_last:
        print('hash of new: {}\nlast saved hash: {}'.
                format(md5, hash_of_last), sep='\n')
        print('City-code byte-data retrieved, proves different from previous.')
        # Save new hash of current version.
        with open(os.path.join(
                '../DATA/CITY_LISTS', 'hash_of_last.txt'), 'w') as f:
            f.write(md5)
        # Report any non-ASCII content to STDOUT and normalize.
        chars = set([i for i in cities])
        for c in chars:
            if c > 122:
                print('Non-ASCII character {} ({}) at position {}.'.
                        format(c, repr(chr(c)), cities.find(c)))
        city_list_filename = ('city_list_normalized_' + U.construct_date() + 
                '.txt')
        normalized = ''.join([chr(char) for char in cities])
        # Here we replace any non-ASCII characters we know about already.
        normalized = normalized.replace(chr(150), '-')
        with open(os.path.join(
                '../DATA/CITY_LISTS', city_list_filename), 'w') as f:
            f.write(normalized)
        print('Normalized city-code data saved.')
    else:
        print('No change in data found.')

def open_last_city_list():
    """Find filename of most recently saved city code list."""
    file_list = glob.glob('../DATA/CITY_LISTS/city_list*')
    filename = file_list[-1]
    return filename.split('/')[-1]

def isolate_city_codes():
    """Get contents of most recently saved city code list, as list of lists."""
    filename = open_last_city_list()
    with open(os.path.join('../DATA/CITY_LISTS', filename), 'r') as f:
        contents = f.read()
    list_of_lines = [line.split('\t') for line in contents.split('\n')[1:]]
    # Latitude and longitude should be numbers
    for i in range(1, len(list_of_lines)-1):
        list_of_lines[i][2] = float(list_of_lines[i][2])
        list_of_lines[i][3] = float(list_of_lines[i][3])
    print('Total number of city codes: {}.'.format(len(list_of_lines)))
    return list_of_lines

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
    # id_hits is now a list of 1-tuples. Convert to plain list and return.
    return [i[0] for i in id_hits]

if __name__ == '__main__':
    get_city_code_list()
