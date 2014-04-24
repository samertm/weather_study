#!/Users/ginaschmalzle/v_env3/bin/python
from mpl_toolkits.basemap import Basemap, cm
import numpy as np
from netCDF4 import Dataset as NetCDFFile
import matplotlib.pyplot as plt
import retrieve

exact_date=20140421  # Define Target date you would like to see

lat=[]; lon=[]; 
maxt_0=[]; maxt_1=[]; maxt_2=[]; maxt_3=[]; maxt_4=[]; maxt_5=[]; maxt_6=[]; maxt_7=[]
diff0_7=[]; diff0_6=[]; diff0_5=[];diff0_4=[]; diff0_3=[];diff0_2=[]; diff0_1=[]

def make_basemap(diff, lon, lat):
	# Make a basic map of the United states
	if diff == diff0_7:
		label = "7 day diff"
		pos = 421
	elif diff == diff0_6:
		label = "6 day diff"
		pos = 422
	elif diff == diff0_5:
		label = "5 day diff"
		pos = 423
	elif diff == diff0_4:
		label = "4 day diff"
		pos = 424
	elif diff == diff0_3:
		label = "3 day diff"
		pos = 425
	elif diff == diff0_2:
		label = "2 day diff"
		pos = 426
	elif diff == diff0_1:
		label = "1 day diff"
		pos = 427
	else:
		label = "huh?"
		diff = diff0_1
		pos = 428


	plt.subplot(pos)
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

	# draw Circles on the map
	# Determine min and max differenced values 
	jet = plt.cm.get_cmap('jet')
	x,y = (m(lon,lat))
	sc = plt.scatter(x, y, c=diff, vmin=mindiff, vmax=maxdiff, cmap=jet, s=8, edgecolors='none' )
	# add colorbar
	plt.colorbar(sc)
	# add title
	plt.title(label)


# Get Forecast data from retrieve.py
x = retrieve.get_single_date_data_from_db(exact_date)
# Define variables
for city in x:
	lat.append(city[0])
	lon.append(city[1])
	maxt_0.append(x[city[0],city[1]][0][0])
	maxt_1.append(x[city[0],city[1]][1][0])
	maxt_2.append(x[city[0],city[1]][2][0])
	maxt_3.append(x[city[0],city[1]][3][0])
	maxt_4.append(x[city[0],city[1]][4][0])
	maxt_5.append(x[city[0],city[1]][5][0])
	maxt_6.append(x[city[0],city[1]][6][0])
	maxt_7.append(x[city[0],city[1]][7][0])
diff0_7=[x1-x2 for x1,x2 in zip(maxt_0,maxt_7)]
diff0_6=[x1-x2 for x1,x2 in zip(maxt_0,maxt_6)]
diff0_5=[x1-x2 for x1,x2 in zip(maxt_0,maxt_5)]
diff0_4=[x1-x2 for x1,x2 in zip(maxt_0,maxt_4)]
diff0_3=[x1-x2 for x1,x2 in zip(maxt_0,maxt_3)]
diff0_2=[x1-x2 for x1,x2 in zip(maxt_0,maxt_2)]
diff0_1=[x1-x2 for x1,x2 in zip(maxt_0,maxt_1)]
# plt.figure determines figure size 
fig = plt.figure(figsize=(15,10))  
mindiff=min(diff0_7)
maxdiff=max(diff0_7)
collection = [diff0_7, diff0_6, diff0_5, diff0_4, diff0_3, diff0_2, diff0_1]
for plot in collection:
	make_basemap(plot, lon, lat)
plt.show()

