#! /usr/bin/python
# explore_response_hashes.py
# David Prager Branner and Gina Schmalzle
# 20140425

"""Explore changes to hash() value of an http.client.HTTPResponse  object."""

import urllib.request
import urllib.error
import hashlib

url = 'http://openweathermap.org/help/city_list.txt'
response_hash_set = set()
counter = 0
while len(response_hash_set) < 100:
    counter += 1
    response = urllib.request.urlopen(url)
    response_hash = hash(response)
    if (response_hash not in response_hash_set):
        response_hash_set.add(response_hash)
        print('{}: {}'.format(counter, response_hash))
print('\nToo many different hashes.\n{}'.format(response_hash_set))
