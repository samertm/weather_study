#!/Users/ginaschmalzle/v_env3/bin/python
from mpl_toolkits.basemap import Basemap, cm
import numpy as np
from netCDF4 import Dataset as NetCDFFile
import matplotlib.pyplot as plt
import mpl_util

def findSubsetIndices(min_lat,max_lat,min_lon,max_lon,lats,lons):
    
    """Array to store the results returned from the function"""
    res=np.zeros((4),dtype=np.float64)
    minLon=min_lon; maxLon=max_lon
    
    distances1 = []; distances2 = []
    indices=[]; index=1
    
    for point in lats:
        s1 = max_lat-point # (vector subtract)
        s2 = min_lat-point # (vector subtract)
        distances1.append((np.dot(s1, s1), point, index))
        distances2.append((np.dot(s2, s2), point, index-1))
        index=index+1
        
    distances1.sort()
    distances2.sort()
    indices.append(distances1[0])
    indices.append(distances2[0])
    
    distances1 = []; distances2 = []; index=1
   
    for point in lons:
        s1 = maxLon-point # (vector subtract)
        s2 = minLon-point # (vector subtract)
        distances1.append((np.dot(s1, s1), point, index))
        distances2.append((np.dot(s2, s2), point, index-1))
        index=index+1
        
    distances1.sort()
    distances2.sort()
    indices.append(distances1[0])
    indices.append(distances2[0])
    
    """ Save final product: max_lat_indices,min_lat_indices,max_lon_indices,min_lon_indices"""
    minJ=indices[1][2]
    maxJ=indices[0][2]
    minI=indices[3][2]
    maxI=indices[2][2]
    
    res[0]=minI; res[1]=maxI; res[2]=minJ; res[3]=maxJ;
    return res

# Add netcdf file
nc = NetCDFFile('./nws_precip_20140101_nc/nws_precip_conus_20140101.nc')
# data from http://water.weather.gov/precip/
prcpvar = nc.variables['amountofprecip']
print (prcpvar[:])
data = 0.01*prcpvar[:]

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
# draw data contours
ny = data.shape[0]     # shape returns the dimensions of the numpy array.  
nx = data.shape[1]	   # Assuming a n rows and m columns, .shape[0] would give n (latitudes) shape[1] gives longitudes 
lons, lats = m.makegrid(nx, ny) # get lat/lons of ny by nx evenly space grid.
x, y = m(lons, lats) # compute map proj coordinates.
# draw filled contours.
clevs = [0,1,2.5,5,7.5,10,15,20,30,40,50,70,100,150,200,250,300,400,500,600,750]
cs = m.contourf(x,y,data,clevs,cmap=cm.s3pcpn)
# add colorbar.
cbar = m.colorbar(cs,location='bottom',pad="5%")
cbar.set_label('mm')
# add title
plt.title("Simple map of United States")
plt.show()

