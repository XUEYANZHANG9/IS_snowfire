
# coding: utf-8

# In[3]:

import xray 
import numpy as np
import sys
import os
import gc 
from snowpack_functions import get_elev_for_lat_lon,import_gridcell_elevation

soil_file = '/raid9/gergel/agg_snowpack/soil_avail.txt'
elev_corr_info = import_gridcell_elevation(soil_file)

#args = sys.argv[1:]
#model = args[0]
#scenario = args[1]
#model = "CNRM-CM5"
#scenario = "historical"

direc = '/raid/gergel/precip' 
file = 'CNRM-CM5_historical_pr.nc'
pr_f = xray.open_dataset(os.path.join(direc,file)) 

lons_new = pr_f['lon'].values[pr_f['lon'].values > 180] - 360
pr_f['lon'] = lons_new 

pr_f['lat'] = np.round(pr_f['lat'], 5)

# cut out conus east of 103 for each variable and also the Canadian headwaters
swe_mask_file = '/raid9/gergel/agg_snowpack/goodleap/SWE/histmeanmask_mod.nc' #  1s are swe, 0s are no swe
swe_mask = xray.open_dataset(swe_mask_file)
# rename dimensions
swe_mask.rename({"Latitude": "lat", "Longitude": "lon", "Time": "time"}, inplace=True)
swe_mask = swe_mask.squeeze()

def slice_dataset_space(ds_array, ds_to_slice):
        '''
        slices second Dataset to fit first Dataset
        '''
        swe_mask_align, array_align = xray.align(ds_array, ds_to_slice, join='inner', copy=False)
        return(array_align)

pr = slice_dataset_space(swe_mask, pr_f)

elevs = np.ndarray(shape=(len(pr.lat),len(pr.lon)),dtype=float) 

pr_sel = pr.sel(time=0) 

for j in np.arange(len(pr.lat)):
    for k in np.arange(len(pr.lon)): 
	if np.isnan(pr_sel['precipitation'].values[j,k]):
		elevs[j,k] = np.nan
	else: 
		elevs[j,k] = get_elev_for_lat_lon(elev_corr_info,np.round(pr_sel.lat.values[j],decimals=5),np.round(pr_sel.lon.values[k],decimals=5)) 
    	print('%f %f' % (j, k)) 

#grid = xray.Dataset()
#lon_da = xray.DataArray(data.lon,dims=('longitude', ), name='lon', attrs={'long_name': 'lon coordinate'}) 
#lat_da = xray.DataArray(data.lat,dims=('latitude', ), name='lat', attrs={'long_name': 'lat coordinate'}) 

#grid['elevations'] = xray.DataArray(elevs, dims=('lat','lon'), name='elevations', coords={'lat':lat_da,'lon':lon_da}, attrs={'long_name': elevations, 'comment': 'elevations taken from vic soil file'})



direc = '/raid/gergel'
filename = 'elevations.npz' 
#grid.to_netcdf(os.path.join(direc,filename))
np.savez(os.path.join(direc,filename),elevs=elevs) 
print('saved dataset to netcdf as %s' %os.path.join(direc,filename)) 
