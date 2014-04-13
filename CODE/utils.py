#! /usr/bin/python
# David Prager Branner
# 20140412

"""Utilities for Weather Study project."""

import os

filename = 'weather_underground_api.ignore'
with open(os.path.join('../DATA', filename), 'r') as f:
    api_key = f.read()

print(api_key)

# The following is not working yet.
def construct_WU_api_req(city='New_York', history=None):
    head = 'http://api.wunderground.com/api/'
    tail = '/geolookup/conditions/q/'
    if city:
        city += '.json'


