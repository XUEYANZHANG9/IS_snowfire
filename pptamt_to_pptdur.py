
# coding: utf-8

# In[3]:

import xray 
import numpy as np
import sys
import os
import gc 

# In[6]:

args = sys.argv[1:]
model = args[0]
scenario = args[1]
#model = "CNRM-CM5"
#scenario = "historical"

direc = '/raid/gergel/%s' % "precip"
pr_file = "%s_%s_%s.nc" % (model,scenario,"pr")
pr = xray.open_dataset(os.path.join(direc,pr_file)) ## load precip

## adjust lat/lon dimensions since the index names are different
lons_new = pr['lon'].values[pr['lon'].values > 180] - 360 
pr['lon'] = lons_new

swe_mask_file = '/raid9/gergel/agg_snowpack/goodleap/SWE/histmeanmask.nc' ## 1s are swe, 0s are no swe 
swe_mask = xray.open_dataset(swe_mask_file)

## rename dimensions
swe_mask.rename({"Latitude": "lat", "Longitude": "lon", "Time": "time"}, inplace=True)

swe_mask = swe_mask.squeeze()

## Dataset join 
swe_mask_align,pr_full = xray.align(swe_mask,pr,join='inner',copy=False)
#swe_mask_align,tmax_align = xray.align(swe_mask,tmax,join='inner',copy=False)

del pr 
gc.collect() 

direc = '/raid/gergel'
pdur_file = 'pduration.nc'
pdur_full = xray.open_dataset(os.path.join(direc,pdur_file)) ## pdur beta parameter for John's transform from Matt Jolly


# In[13]:

# pr_arr = pr_full['precipitation'].values
for j in np.arange(len(pr_full.lat)):
    for k in np.arange(len(pr_full.lon)):
        if np.isnan(pr_full['precipitation'].values[0,j,k]) == False: 
            lon_ind = np.argmin(np.abs(pdur_full.lon - pr_full.lon[k]))
            lat_ind = np.argmin(np.abs(pdur_full.lat - pr_full.lat[j]))
            beta = np.float(pdur_full.isel_points(lon=[lon_ind],lat=[lat_ind])['pdur'])
            #u = pr_arr[:,j,k]
            # u = np.round(24 * (1 - (np.exp(-beta*pr_full['precipitation'].values[:,j,k]))))
	    pr_full['precipitation'].values[:,j,k] = np.round(24 * (1 - (np.exp(-beta*pr_full['precipitation'].values[:,j,k]))))
# In[ ]:

#pr_full['precipitation'].values = pr_arr
direc = '/raid/gergel/pptdur'
filename = '%s_%s.nc' % (model,scenario)
pr_full.to_netcdf(os.path.join(direc,filename))
print('saved dataset to netcdf as %s' %os.path.join(direc,filename)) 
