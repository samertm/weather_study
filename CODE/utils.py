#! /usr/bin/python
# David Prager Branner
# 20140411, abandoned; does not compile

"""Utilities for Weather Study project."""

with open() as f:
    api_key = 

def construct_WU_api_req(city='New_York', history=None):
    head = 'http://api.wunderground.com/api/'
    tail = '/geolookup/conditions/q/'
    if city:
        city += '.json'


