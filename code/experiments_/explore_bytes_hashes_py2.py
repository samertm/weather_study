#! /usr/bin/python
# explore_bytes_hashes_py2.py
# David Prager Branner and Gina Schmalzle
# 20140425

"""Explore changes to the hash() and md5 values of bytes objects."""

import urllib2
import hashlib

url = 'http://openweathermap.org/help/city_list.txt'
hash_set = set()
md5_set = set()
counter = 0
while len(hash_set) < 100 or len(md5_set) < 100 or len(response_hash_set) < 100:
    counter += 1
    response = urllib2.urlopen(url)
    content = response.read()
    the_hash = hash(content)
    the_md5 = hashlib.md5(content).hexdigest()
    if (the_hash not in hash_set or 
            the_md5 not in md5_set):
        hash_set.add(the_hash)
        md5_set.add(the_md5)
        print('{}: {:>20d}, {}'.
                format(counter, the_hash, the_md5))
print('\nToo many different hashes.\n{}\n\n{}'.
        format(hash_set, md5_set))
