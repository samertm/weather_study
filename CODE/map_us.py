#!/Users/ginaschmalzle/v_env3/bin/python
from mpl_toolkits.basemap import Basemap, cm
import numpy as np
from netCDF4 import Dataset as NetCDFFile
import matplotlib.pyplot as plt
import retrieve
import ast
pick_data='maxt'  # Either maxt, mint, rain or snow
exact_date=20140422  # Define Target date you would like to see

lat=[]; lon=[]; 
a0=[]; a1=[]; a2=[]; a3=[]; a4=[]; a5=[]; a6=[]; a7=[]; a8=[]; a9=[]
diff0_8=[]; diff0_9=[]; diff0_7=[]; diff0_6=[]; diff0_5=[];diff0_4=[]; diff0_3=[];diff0_2=[]; diff0_1=[]

def make_basemap(diff, lon, lat, mindiff, maxdiff):
	# Make a basic map of the United states
	if diff == diff0_1:
		label = "1 day diff"
		pos = 331
	elif diff == diff0_2:
		label = "2 day diff"
		pos = 332
	elif diff == diff0_3:
		label = "3 day diff"
		pos = 333
	elif diff == diff0_4:
		label = "4 day diff"
		pos = 334
	elif diff == diff0_5:
		label = "5 day diff"
		pos = 335
	elif diff == diff0_6:
		label = "6 day diff"
		pos = 336
	elif diff == diff0_7:
		label = "7 day diff"
		pos = 337
	elif diff == diff0_8:
		label = "8 day diff"
		pos = 338
	elif diff == diff0_9:
		label = "9 day diff"
		pos = 339
	else:
		label = "huh?"
		diff = diff0_1
		pos = 339


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
#x = retrieve.get_single_date_data_from_db(exact_date)
#y=str(x)
#with open('x.py','w') as f:
#	f.write(x)
with open('x.py','r') as f:
	x = f.read()
x = ast.literal_eval(x)
#print(x==z)
# Define variables
for city in x:
	lat.append(city[0])
	lon.append(city[1])
	if pick_data=='maxt':
		a0.append(x[city[0],city[1]][0][0])
		a1.append(x[city[0],city[1]][1][0])
		a2.append(x[city[0],city[1]][2][0])
		a3.append(x[city[0],city[1]][3][0])
		a4.append(x[city[0],city[1]][4][0])
		a5.append(x[city[0],city[1]][5][0])
		a6.append(x[city[0],city[1]][6][0])
		a7.append(x[city[0],city[1]][7][0])
		a8.append(x[city[0],city[1]][8][0])
		a9.append(x[city[0],city[1]][9][0])
	elif pick_data=='mint':
		a0.append(x[city[0],city[1]][0][1])
		a1.append(x[city[0],city[1]][1][1])
		a2.append(x[city[0],city[1]][2][1])
		a3.append(x[city[0],city[1]][3][1])
		a4.append(x[city[0],city[1]][4][1])
		a5.append(x[city[0],city[1]][5][1])
		a6.append(x[city[0],city[1]][6][1])
		a7.append(x[city[0],city[1]][7][1])
		a8.append(x[city[0],city[1]][8][1])
		a9.append(x[city[0],city[1]][9][1])
	elif pick_data=='rain':
		a0.append(x[city[0],city[1]][0][2])
		a1.append(x[city[0],city[1]][1][2])
		a2.append(x[city[0],city[1]][2][2])
		a3.append(x[city[0],city[1]][3][2])
		a4.append(x[city[0],city[1]][4][2])
		a5.append(x[city[0],city[1]][5][2])
		a6.append(x[city[0],city[1]][6][2])
		a7.append(x[city[0],city[1]][7][2])
		a8.append(x[city[0],city[1]][8][2])
		a9.append(x[city[0],city[1]][9][2])
	elif pick_data=='snow':
		a0.append(x[city[0],city[1]][0][3])
		a1.append(x[city[0],city[1]][1][3])
		a2.append(x[city[0],city[1]][2][3])
		a3.append(x[city[0],city[1]][3][3])
		a4.append(x[city[0],city[1]][4][3])
		a5.append(x[city[0],city[1]][5][3])
		a6.append(x[city[0],city[1]][6][3])
		a7.append(x[city[0],city[1]][7][3])
		a8.append(x[city[0],city[1]][8][3])
		a9.append(x[city[0],city[1]][9][3])
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
# plt.figure determines figure size 
fig = plt.figure(figsize=(20,10)) 

temp=str(exact_date)
maintitle=(pick_data)
plt.suptitle(maintitle, fontsize=18) 
mindiff=min(diff0_8)
maxdiff=max(diff0_8)
print('MinDiff = ',mindiff,'MaxDiff = ', maxdiff)
collection = [diff0_8, diff0_7, diff0_6, diff0_5, diff0_4, diff0_3, diff0_2, diff0_1]
for plot in collection:
	make_basemap(plot, lon, lat, mindiff, maxdiff)
#plt.savefig('MinT20140422.png')
plt.show()

