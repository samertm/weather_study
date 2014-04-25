#! /usr/bin/python
# explore_bytes_hashes.py
# David Prager Branner and Gina Schmalzle
# 20140425

"""Explore changes to the hash() and md5 values of bytes objects."""

import urllib.request
import urllib.error
import hashlib

url = 'http://openweathermap.org/help/city_list.txt'
hash_set = set()
md5_set = set()
# response_hash_set = set()
counter = 0
while len(hash_set) < 100 or len(md5_set) < 100 or len(response_hash_set) < 100:
    counter += 1
    response = urllib.request.urlopen(url)
    content = response.read()
#    response_hash = hash(response)
    the_hash = hash(content)
    the_md5 = hashlib.md5(content).hexdigest()
    if (the_hash not in hash_set or 
            the_md5 not in md5_set):
#            the_md5 not in md5_set or 
#            response_hash not in response_hash_set):
        hash_set.add(the_hash)
        md5_set.add(the_md5)
#        response_hash_set.add(response_hash)
        print('{}: {:>20d}, {}'.
                format(counter, the_hash, the_md5))
print('\nToo many different hashes.\n{}\n\n{}'.
        format(hash_set, md5_set))
#        print('{}: {:>20d}, {}, {}'.
#                format(counter, the_hash, the_md5, response_hash))
#print('\nToo many different hashes.\n{}\n\n{}\n\n{}'.
#        format(hash_set, md5_set, response_hash_set))
