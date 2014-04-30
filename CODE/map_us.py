#! /usr/bin/env python
# map_us.py
# David Prager Branner and Gina Schmalzle
# 20140429, works

"""Generate plots of forecast-differences, using list comprehensions."""

from mpl_toolkits.basemap import Basemap, cm
import matplotlib.gridspec as gridspec
import numpy as np
import matplotlib.pyplot as plt
import retrieve
import os
import time
import argparse

def make_single_basemap(diff, day, lon, lat, mindiff, maxdiff, hist=True):
    """Create basic map of U.S. and add forecast-difference information."""
    # Find number of days of forecasting and construct label.
    label = str(day) + ' day diff'
    # Begin histogram creation.
    if hist:
        gs=gridspec.GridSpec(1,2,width_ratios=[4,1], height_ratios=[8,1])
        plt.subplot(gs[0])
    # Create Mercator Projection Basemap instance.
    m = Basemap(
            projection='merc', llcrnrlat=25, urcrnrlat=50, llcrnrlon=-130,
            urcrnrlon=-60, rsphere=6371200., resolution='l',
            area_thresh=10000)
    # Draw coastlines, state and country boundaries, edge of map.
    m.drawcoastlines()
    m.drawstates()
    m.drawcountries()
    # Draw parallels.
    parallels = np.arange(0., 90, 10.)
    m.drawparallels(parallels, labels=[1, 0, 0, 0], fontsize=10)
    # Draw meridians.
    meridians = np.arange(180., 360., 10.)
    m.drawmeridians(meridians, labels=[0, 0, 0, 1], fontsize=10)
    # Plot datapoints as circles on the map.
    jet = plt.cm.get_cmap('jet')
    x, y = m(lon,lat)
    plt.scatter(x, y, c=diff, vmin=mindiff, vmax=maxdiff, cmap=jet, s=20,
            edgecolors='none')
    # Add colorbar.
    plt.colorbar(label=topic['clabel'], shrink=0.5)
    # Add title.
    plt.title(label)
    # Add histogram.
    if hist:
        plt.subplot(gs[1])
        binwidth = 1.0
        plt.hist(diff, bins = round(maxdiff-mindiff/binwidth), align='mid',
                orientation='horizontal')
        plt.ylim(mindiff, maxdiff)
        plt.xlim(0,2000)

start_time = time.time()
parser = argparse.ArgumentParser()                                              
parser.add_argument('date', type=int, help='enter single date')
args = parser.parse_args()
print(args)
feature = 'maxt'  # Either maxt, mint, rain or snow
if not args.date:
    args.date = 20140422
exact_date = args.date
file_type = 'png'
figuresize = (20, 10)
res = 600
# Make sure ../OUTPUT exists or create it.
if not os.path.exists('../OUTPUT'):
    os.makedirs('../OUTPUT')
    print('Created directory OUTPUT', end='\n\n')
# Prepare materials appropriate to different features..
temp_header = '{} Temperature Difference (degrees) for '+str(exact_date)
precip_header = '{} level difference (mm) for '+str(exact_date)
temp_label = '{} (obs?) - {} (Model?), degrees'
precip_label = '{} (obs?) - {} (Model?), degrees'
topics = {
        'maxt': {'header': temp_header.format('Maximum'),
            'clabel': temp_label.format('MaxT', 'MaxT'),
            'position': 0},
        'mint': {'header': temp_header.format('Minimum'),
            'clabel': temp_label.format('MinT', 'MinT'),
            'position': 1},
        'rain': {'header': precip_header.format('Rain'),
            'clabel': precip_label.format('rain', 'rain'),
            'position': 2},
        'snow': {'header': precip_header.format('Snow'),
            'clabel': precip_label.format('snow', 'snow'),
            'position': 3},
        'other': {'header': 'Not sure', 'clabel': 'Not sure'},}
if feature in topics:
    topic = topics[feature]
else:
    print('{} not found in our resources. Exiting.'.format(topic))
# Get Forecast data from retrieve.py
retrieved_data = retrieve.get_single_date_data_from_db(
        exact_date, to_print=False)
# Define variables
days = range(10) # QQQ ultimately we want as many places as necessary. 15?
# Lat and lon are needed as distinct lists.
lat = [city[0] for city in retrieved_data]
lon = [city[1] for city in retrieved_data]
forecasts = [[retrieved_data[city][day][topic['position']]
            for city in zip(lat, lon)]
            for day in days]
# Formerly "a" lists were lists of forecasts from a specific day and for a
# specific future day. The following line tested that the list comprehension
# "forecasts" replaced the "a" lists exactly.
#print('Claim: forecasts == [a0, a1, a2, a3, a4, a5, a6, a7, a8, a9]: {}.'.
#        format(forecasts == [a0, a1, a2, a3, a4, a5, a6, a7, a8, a9]))
# QQQ Ultimately, replace "forecasts[1:9]" with code to ignore "None" content.
differences = [[target_fc - prior_fc for target_fc, prior_fc in
        zip(forecasts[0], forecast)] for forecast in forecasts[1:9]]
# Formerly "diff" lists held the differences between correponding forecasts.
# The following line tested that the list comprehension "differences" replaced
# the "diff" lists exactly.
#print('Claim: differences == [diff0_1, diff0_2, diff0_3, diff0_4, diff0_5, '
#        'diff0_6, diff0_7, diff0_8]: {}.'.
#        format(differences == [diff0_1, diff0_2, diff0_3, diff0_4, diff0_5,
#            diff0_6, diff0_7, diff0_8]))
plt.suptitle(topic['header'], fontsize=18)
mindiff = round(min(differences[-1]), 2)
maxdiff = round(max(differences[-1]), 2)
print('MinDiff = {}, MaxDiff = {}.'.format(mindiff, maxdiff))
for day, plot in enumerate(reversed(differences)):
    # plt.figure determines figure size
    plt.figure(figsize=figuresize)
    make_single_basemap(plot, str(8 - day), lon, lat, mindiff, maxdiff)
    filename = (str(exact_date) + '_' + feature + '_' + str(8 - day) +
            '.' + file_type)
    plt.savefig('../OUTPUT/' + filename, dpi=res)
end_time = time.time()
print('Total time elapsed: {} seconds.'.format(round(end_time-start_time)))
