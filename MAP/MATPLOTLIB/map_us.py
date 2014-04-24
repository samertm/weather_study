#!/Users/ginaschmalzle/v_env3/bin/python
from mpl_toolkits.basemap import Basemap, cm
import numpy as np
from netCDF4 import Dataset as NetCDFFile
import matplotlib.pyplot as plt
import mpl_util
import retrieve
# Get Forecast data from retrieve.py
x = retrieve.get_weather_data_from_db(start_date=20140423, end_date=20140423)

for i in x:
	print(x[i])
# Make a basic map of the United states
# plt.figure determines figure size 
fig = plt.figure(figsize=(10,10))  
# create Mercator Projection Basemap instance.
m = Basemap(projection='merc',\
            llcrnrlat=25,urcrnrlat=50,\
            llcrnrlon=-130,urcrnrlon=-60,\
            rsphere=6371200.,resolution='l',area_thresh=10000)
# draw coastlines, state and country boundaries, edge of map.
m.drawcoastlines()
m.drawstates()
m.drawcountries()
# draw parallels.
parallels = np.arange(0.,90,10.)
m.drawparallels(parallels,labels=[1,0,0,0],fontsize=10)
# draw meridians
meridians = np.arange(180.,360.,10.)
m.drawmeridians(meridians,labels=[0,0,0,1],fontsize=10)
# add title
plt.title("Simple map of United States")
plt.show()

