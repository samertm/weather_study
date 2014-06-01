#! /usr/bin/env python
# map_us.py
# David Prager Branner and Gina Schmalzle
# 20140428, in progress

from mpl_toolkits.basemap import Basemap, cm
import numpy as np
from netCDF4 import Dataset as NetCDFFile
import matplotlib.pyplot as plt
import retrieve
import os
import time

class Plotter():
    def __init__(self):
        pass

    def make_single_basemap(self, diff, lon, lat, mindiff, maxdiff):
        # Make a basic map of the United states
        if diff == diff0_1:
            label = "1 day diff"
        elif diff == diff0_2:
            label = "2 day diff"
        elif diff == diff0_3:
            label = "3 day diff"
        elif diff == diff0_4:
            label = "4 day diff"
        elif diff == diff0_5:
            label = "5 day diff"
        elif diff == diff0_6:
            label = "6 day diff"
        elif diff == diff0_7:
            label = "7 day diff"
        elif diff == diff0_8:
            label = "8 day diff"
        elif diff == diff0_9:
            label = "9 day diff"
        else:
            label = "huh?"
            diff = diff0_1
        # create Mercator Projection Basemap instance.
        m = Basemap(
                projection='merc', llcrnrlat=25, urcrnrlat=50, llcrnrlon=-130,
                urcrnrlon=-60, rsphere=6371200., resolution='l',
                area_thresh=10000)
        # draw coastlines, state and country boundaries, edge of map.
        m.drawcoastlines()
        m.drawstates()
        m.drawcountries()
        # draw parallels.
        parallels = np.arange(0., 90, 10.)
        m.drawparallels(parallels, labels=[1, 0, 0, 0], fontsize=10)
        # draw meridians
        meridians = np.arange(180., 360., 10.)
        m.drawmeridians(meridians, labels=[0, 0, 0, 1], fontsize=10)
        # draw Circles on the map
        # Determine min and max differenced values
        jet = plt.cm.get_cmap('jet')
        x,y = m(lon,lat)
        plt.scatter(x, y, c=diff, vmin=mindiff, vmax=maxdiff, cmap=jet, s=20,
                edgecolors='none')
        # add colorbar
        plt.colorbar(label=words['clabel'], shrink=0.5)
        # add title
        plt.title(label)

start_time = time.time()
pick_data = 'maxt'  # Either maxt, mint, rain or snow
exact_date = 20140422  # Define Target date you would like to see
file_type = 'png'
figuresize = (20, 10)
res = 600
# Make sure ../OUTPUT exists or create it.
if not os.path.exists('../OUTPUT'):
    os.makedirs('../OUTPUT')
    print('Created directory OUTPUT', end='\n\n')
temp_header = '{} Temperature Difference (degrees) for '+str(exact_date)
precip_header = '{} level difference (mm) for '+str(exact_date)
temp_label = '{} (obs?) - {} (Model?), degrees'
precip_label = '{} (obs?) - {} (Model?), degrees'
data_dict = {
        'maxt': {'header': temp_header.format('Maximum'),
            'clabel': temp_label.format('MaxT', 'MaxT')},
        'mint': {'header': temp_header.format('Minimum'),
            'clabel': temp_label.format('MinT', 'MinT')},
        'rain': {'header': precip_header.format('Rain'),
            'clabel': precip_label.format('rain', 'rain')},
        'snow': {'header': precip_header.format('Snow'),
            'clabel': precip_label.format('snow', 'snow')},
        'other': {'header': 'Not sure', 'clabel': 'Not sure'},}
if pick_data in data_dict:
    words = data_dict[pick_data]
else:
    words = data_dict['other']
#if pick_data == 'maxt':
#        header='Maximum Temperature Difference (degrees) for '+str(exact_date)
#        clabel='MaxT (obs) - MaxT (Model), degrees' 
#elif pick_data == 'mint':
#        header='Minimum Temperature Difference (degrees) for '+str(exact_date)
#        clabel='MinT (obs) - MinT (Model), degrees' 
#elif pick_data == 'snow':
#        header='Snow level difference (mm) for '+str(exact_date)
#        clabel='snow (obs) - snow (Model), mm' 
#elif pick_data == 'snow':
#        header='Rain level difference (mm) for '+str(exact_date)
#        clabel='rain (obs) - rain (Model), mm' 
#else:
#        header='Not sure'
#        clabel='Not sure'
# lat=[]; lon=[];
a0=[]; a1=[]; a2=[]; a3=[]; a4=[]; a5=[]; a6=[]; a7=[]; a8=[]; a9=[]
diff0_8=[]; diff0_9=[]; diff0_7=[]; diff0_6=[]; diff0_5=[];diff0_4=[]; diff0_3=[];diff0_2=[]; diff0_1=[]
# Get Forecast data from retrieve.py
x = retrieve.get_single_date_data_from_db(exact_date, to_print=False)
# Define variables
lat = [city[0] for city in x]
lon = [city[1] for city in x]
for city in x:
#        lat.append(city[0])
#        lon.append(city[1])
        if pick_data=='maxt':
            # here we replace "x[city[0],city[1]]" => "x[city[0:2]]"
#            print(x[city[0:2]], x[city[0],city[1]])
            a0.append(x[city[0:2]][0][0])
            a1.append(x[city[0:2]][1][0])
            a2.append(x[city[0:2]][2][0])
            a3.append(x[city[0:2]][3][0])
            a4.append(x[city[0:2]][4][0])
            a5.append(x[city[0:2]][5][0])
            a6.append(x[city[0:2]][6][0])
            a7.append(x[city[0:2]][7][0])
            a8.append(x[city[0:2]][8][0])
            a9.append(x[city[0:2]][9][0])
        elif pick_data=='mint':
                a0.append(x[city[0:2]][0][1])
                a1.append(x[city[0:2]][1][1])
                a2.append(x[city[0:2]][2][1])
                a3.append(x[city[0:2]][3][1])
                a4.append(x[city[0:2]][4][1])
                a5.append(x[city[0:2]][5][1])
                a6.append(x[city[0:2]][6][1])
                a7.append(x[city[0:2]][7][1])
                a8.append(x[city[0:2]][8][1])
                a9.append(x[city[0:2]][9][1])
        elif pick_data=='rain':
                a0.append(x[city[0:2]][0][2])
                a1.append(x[city[0:2]][1][2])
                a2.append(x[city[0:2]][2][2])
                a3.append(x[city[0:2]][3][2])
                a4.append(x[city[0:2]][4][2])
                a5.append(x[city[0:2]][5][2])
                a6.append(x[city[0:2]][6][2])
                a7.append(x[city[0:2]][7][2])
                a8.append(x[city[0:2]][8][2])
                a9.append(x[city[0:2]][9][2])
        elif pick_data=='snow':
                a0.append(x[city[0:2]][0][3])
                a1.append(x[city[0:2]][1][3])
                a2.append(x[city[0:2]][2][3])
                a3.append(x[city[0:2]][3][3])
                a4.append(x[city[0:2]][4][3])
                a5.append(x[city[0:2]][5][3])
                a6.append(x[city[0:2]][6][3])
                a7.append(x[city[0:2]][7][3])
                a8.append(x[city[0:2]][8][3])
                a9.append(x[city[0:2]][9][3])
        else:
                print("Input error. What data?")
#diff0_9=[x1-x2 for x1,x2 in zip(a0,a9)]
diff0_8=[x1-x2 for x1,x2 in zip(a0,a8)]
diff0_7=[x1-x2 for x1,x2 in zip(a0,a7)]
diff0_6=[x1-x2 for x1,x2 in zip(a0,a6)]
diff0_5=[x1-x2 for x1,x2 in zip(a0,a5)]
diff0_4=[x1-x2 for x1,x2 in zip(a0,a4)]
diff0_3=[x1-x2 for x1,x2 in zip(a0,a3)]
diff0_2=[x1-x2 for x1,x2 in zip(a0,a2)]
diff0_1=[x1-x2 for x1,x2 in zip(a0,a1)]

plt.suptitle(words['header'], fontsize=18)
mindiff = round(min(diff0_8), 2)
maxdiff = round(max(diff0_8), 2)
print('MinDiff = {}, MaxDiff = {}.'.format(mindiff, maxdiff))
collection = [diff0_8, diff0_7, diff0_6, diff0_5, diff0_4, diff0_3, 
        diff0_2, diff0_1]
for i,plot in enumerate(collection):
    plotter = Plotter()
    # plt.figure determines figure size
    plt.figure(figsize=figuresize)
    plotter.make_single_basemap(plot, lon, lat, mindiff, maxdiff)
    filename = (str(exact_date) + '_' + pick_data + '_' + str(8 - i) + 
            '.' + file_type)
    plt.savefig('../OUTPUT/' + filename, dpi=res)
end_time = time.time()
print('Total time elapsed: {} seconds.'.format(round(end_time-start_time)))
