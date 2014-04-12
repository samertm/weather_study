#!/usr/bin/python
# try_ndfd.py
# David Prager Branner and Gina Schmalzle
# 20140412

"""Make preliminary experiments with XML/ReST calls to NDFD."""

# Note that we are only getting five future days' forecast, even when we ask
# for much more than that.

import urllib
import pprint

def main():
    # Unsummarized Data for a Subgrid
    url = 'http://graphical.weather.gov/xml/sample_products/browser_interface/ndfdXMLclient.php?lat=38.99&lon=-77.01&product=time-series&end=2014-04-21T00:00:00&maxt=maxt&mint=mint'
    data = urllib.request.urlopen(url)
    pprint.pprint(data.read())



#    url = 'http://graphical.weather.gov/xml/sample_products/browser_interface/ndfdXMLclient.php?lat=38.99&lon=-77.01&product=time-series&end=2014-04-20T00:00:00&maxt=maxt&mint=mint'
