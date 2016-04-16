
# coding: utf-8

# In[1]:

#get_ipython().magic(u'matplotlib inline')
import matplotlib 
matplotlib.use('Agg')
import xarray as xray 
import os
import numpy as np
import sys
import pandas as pd
import matplotlib.pyplot as plt
from dfm_functions import make_map,make_mask, cmap_discretize 

fs = 30 ## fontsize
nbins = 11
lp = 55
dpi = 150

# models = ['CNRM-CM5','NorESM1-M','IPSL-CM5A-MR','CanESM2','CCSM4','HadGEM2-CC365',
                   'HadGEM2-ES365','MIROC5','bcc-csm1-1-m','CSIRO-Mk3-6-0']
models = ['CNRM-CM5'] 
scenarios = ['historical', 'rcp85']
chunks = ['1980s', '2050s']

direc = '/raid9/gergel/agg_snowpack/goodleap/'
filename = 'tmp_%s_TotalSoilMoist_%s.nc' % ("CNRM-CM5", "historical")
ds = xray.open_dataset(os.path.join(direc, filename))

# mask domain
mask_domain_mtns = make_mask('/raid9/gergel/agg_snowpack/gridcells_is_paper/mountains', ds.Latitude, ds.Longitude)
mask_domain_lowlands = make_mask('/raid9/gergel/agg_snowpack/gridcells_is_paper/lowlands', ds.Latitude, ds.Longitude)

# In[14]:
f, axes = plt.subplots(nrows=2, ncols=2, figsize=(30, 30))

rows = [0, 1, 0, 1] 
cols = [0, 0, 1, 1] 

for i in np.arange(len(rows)):

	ax = axes[rows,cols] 
	plt.sca(ax)

	if i < 2: 
	
	# mask domain
		for model in models: 
    			direc = '/raid9/gergel/agg_snowpack/goodleap/' 
    			filename = 'tmp_%s_TotalSoilMoist_%s.nc' % (model, "historical")
			ds = xray.open_dataset(os.path.join(direc, filename))
			ds_hist = ds['SoilMoist'].sel(Time=slice('1969-10-1', '1999-9-30'))
                        ds_hist_gb_mean = ds_hist.groupby('Time.month').mean('Time')
                        ds_hist_gb_min = ds_hist.groupby('Time.month').min('Time')
                        ds_summer_mean_hist = (ds_hist_gb_mean.sel(month=6) + ds_hist_gb_mean.sel(month=7) + ds_hist_gb_mean.sel(month=8)) / 3.0
                        ds_summer_min =  (ds_hist_gb_min.sel(month=6) + ds_hist_gb_min.sel(month=7) + ds_hist_gb_min.sel(month=8)) / 3.0
    			ds_summer = ds_summer_mean_hist - ds_summer_min		
	
			if i == 1:
				filename = 'tmp_%s_TotalSoilMoist_%s.nc' % (model, "rcp85")
				ds = xray.open_dataset(os.path.join(direc, filename))
 
    				ds_fut = ds['SoilMoist'].sel(Time=slice('2039-10-1', '2069-9-30'))
				ds_fut = ds_fut.groupby('Time.month').mean('Time')
				ds_fut_mean = (ds_fut.sel(month=6) + ds_fut.sel(month=7) + ds_fut.sel(month=8)) / 3.0 
    		 		ds_summer = ds_fut_mean - ds_summer_min
		
    			
			if (model == "CNRM-CM5"):
        			ds_avg = ds_summer 
    			else: 
        			ds_avg += ds_summer

	# calculate ensemble average of gcms
	ds_ens = ds_avg / 10.0
	if i == 0:   
		ds_ens_hist = ds_ens 
	elif i == 1:  
		ds_ens_fut = ds_ens 

	else: 

	ds_ens = ds_ens_fut - ds_ens hist  
	
# plot 

m = make_map(fs, label_parallels=True)

vmax = 330
vmin = 0

# trim off whitespace
ds_ens = ds_ens.sel(Latitude=slice(31,49.03), Longitude=slice(ds_ens.Longitude.min(), ds_ens.Longitude.max()))
x,y = m(ds_ens.Longitude, ds_ens.Latitude)
#img = ds_ens.plot(ax=ax, vmin=vmin, vmax=vmax, add_labels=False, cmap='viridis', add_colorbar=False)
img = m.pcolormesh(x, y, ds_ens.to_masked_array(), cmap='viridis', vmin=vmin, vmax=vmax) 
cbar = plt.colorbar(img)
cbar.set_ticks([np.linspace(vmin, vmax, 6, endpoint=True, dtype='int')])
cbar.set_label('Historical \n Soil \n Moisture \n Storage \n [mm]', rotation='horizontal', labelpad=lp)
ax.set_title('1970-1999') 
ax.set_ylabel('Latitude', labelpad=20) 
font = {'size' : fs}
plt.rc('font', **font)

################## 

ax = axes[0,1]
plt.sca(ax)

# mask domain
#models = ['CNRM-CM5']
for model in models:
    direc = '/raid9/gergel/agg_snowpack/goodleap/'
    filename = 'tmp_%s_TotalSoilMoist_%s.nc' % (model, "rcp85")
    ds = xray.open_dataset(os.path.join(direc, filename))
    ds_hist = ds['SoilMoist'].sel(Time=slice('2039-10-1', '2069-9-30'))
    ds_hist_gb_mean = ds_hist.groupby('Time.month').mean('Time')
    ds_hist_gb_min = ds_hist.groupby('Time.month').min('Time')
    ds_summer_mean = (ds_hist_gb_mean.sel(month=6) + ds_hist_gb_mean.sel(month=7) + ds_hist_gb_mean.sel(month=8)) / 3.0
    ds_summer_min =  (ds_hist_gb_min.sel(month=6) + ds_hist_gb_min.sel(month=7) + ds_hist_gb_min.sel(month=8)) / 3.0
    ds_summer = ds_summer_mean - ds_summer_min

    # mask domain
    mask_domain = make_mask('/raid9/gergel/agg_snowpack/gridcells_is_paper/mountains',
                        ds_summer.Latitude,
                        ds_summer.Longitude) # ds.lat and ds.lon are lat and lon dimensions of dataset to be masked 
    ds_summer = ds_summer.where(mask_domain == 1)
    if (model == "CNRM-CM5"):
        ds_avg = ds_summer
    else:
        ds_avg += ds_summer
# calculate ensemble average of gcms
ds_ens = ds_avg / 10.0
ds_ens = ds_ens - ds_ens_hist 
# plot 

m = make_map(fs)
'''
vmax = ds_ens.max(['Latitude','Longitude'])
vmin = ds_ens.min(['Latitude','Longitude'])
'''
vmax = 100
vmin = -100

# trim off whitespace
ds_ens = ds_ens.sel(Latitude=slice(31,49.03), Longitude=slice(ds_ens.Longitude.min(), ds_ens.Longitude.max()))
x,y = m(ds_ens.Longitude, ds_ens.Latitude)
# img = ds_ens.plot(ax=ax, vmin=vmin, vmax=vmax, cmap='bwr_r', add_labels=False, add_colorbar=False)
img = m.pcolormesh(x, y, ds_ens.to_masked_array(), vmin=vmin, vmax=vmax, cmap='bwr_r') 

cbar = plt.colorbar(img)
cbar.set_ticks([np.linspace(vmin, vmax, 5, endpoint=True, dtype='int')])
cbar.set_label('Change \n in \n Soil \n Moisture \n Storage \n [mm]', rotation='horizontal', labelpad=lp)
ax.set_title('RCP 8.5 2050s')
font = {'size' : fs}
plt.rc('font', **font)

##################### 

ax = axes[1,0]
plt.sca(ax)

# mask domain
#models = ['CNRM-CM5']
for model in models:
    direc = '/raid9/gergel/agg_snowpack/goodleap/'
    filename = 'tmp_%s_TotalSoilMoist_%s.nc' % (model, "historical")
    ds = xray.open_dataset(os.path.join(direc, filename))
    ds_hist = ds['SoilMoist'].sel(Time=slice('1969-10-1', '1999-9-30'))
    ds_hist_gb_mean = ds_hist.groupby('Time.month').mean('Time')
    ds_hist_gb_min = ds_hist.groupby('Time.month').min('Time')
    ds_summer_mean = (ds_hist_gb_mean.sel(month=6) + ds_hist_gb_mean.sel(month=7) + ds_hist_gb_mean.sel(month=8)) / 3.0
    ds_summer_min =  (ds_hist_gb_min.sel(month=6) + ds_hist_gb_min.sel(month=7) + ds_hist_gb_min.sel(month=8)) / 3.0
    ds_summer = ds_summer_mean - ds_summer_min

    # mask domain
    mask_domain = make_mask('/raid9/gergel/agg_snowpack/gridcells_is_paper/lowlands',
                        ds_summer.Latitude,
                        ds_summer.Longitude) # ds.lat and ds.lon are lat and lon dimensions of dataset to be masked 
    ds_summer = ds_summer.where(mask_domain == 1)
    if (model == "CNRM-CM5"):
        ds_avg = ds_summer
    else:
        ds_avg += ds_summer
# calculate ensemble average of gcms
ds_ens = ds_avg / 10.0
ds_ens_hist = ds_ens
# plot 

m = make_map(fs, label_parallels=True, label_meridians=True)
'''
vmax = ds_ens.max(['Latitude','Longitude'])
vmin = ds_ens.min(['Latitude','Longitude'])
'''
vmax = 240
vmin = 0

# trim off whitespace
ds_ens = ds_ens.sel(Latitude=slice(31,49.03), Longitude=slice(ds_ens.Longitude.min(), ds_ens.Longitude.max()))
x,y = m(ds_ens.Longitude, ds_ens.Latitude)
# img = ds_ens.plot(ax=ax, vmin=vmin, vmax=vmax, add_labels=False, cmap='viridis', add_colorbar=False)
img = m.pcolormesh(x, y, ds_ens.to_masked_array(), cmap='viridis', vmin=vmin, vmax=vmax) 

cbar = plt.colorbar(img)
cbar.set_ticks([np.linspace(vmin, vmax, 6, endpoint=True, dtype='int')])
cbar.set_label('Historical \n Soil \n Moisture \n Storage \n [mm]', rotation='horizontal', labelpad=lp)
ax.set_ylabel('Latitude', labelpad=20)
ax.set_xlabel('Longitude', labelpad=20) 
font = {'size' : fs}
plt.rc('font', **font)

###################

ax = axes[1,1]
plt.sca(ax)

# mask domain
#models = ['CNRM-CM5']
for model in models:
    direc = '/raid9/gergel/agg_snowpack/goodleap/'
    filename = 'tmp_%s_TotalSoilMoist_%s.nc' % (model, "rcp85")
    ds = xray.open_dataset(os.path.join(direc, filename))
    ds_hist = ds['SoilMoist'].sel(Time=slice('2039-10-1', '2069-9-30'))
    ds_hist_gb_mean = ds_hist.groupby('Time.month').mean('Time')
    ds_hist_gb_min = ds_hist.groupby('Time.month').min('Time')
    ds_summer_mean = (ds_hist_gb_mean.sel(month=6) + ds_hist_gb_mean.sel(month=7) + ds_hist_gb_mean.sel(month=8)) / 3.0
    ds_summer_min =  (ds_hist_gb_min.sel(month=6) + ds_hist_gb_min.sel(month=7) + ds_hist_gb_min.sel(month=8)) / 3.0
    ds_summer = ds_summer_mean - ds_summer_min

    # mask domain
    mask_domain = make_mask('/raid9/gergel/agg_snowpack/gridcells_is_paper/lowlands',
                        ds_summer.Latitude,
                        ds_summer.Longitude) # ds.lat and ds.lon are lat and lon dimensions of dataset to be masked 
    ds_summer = ds_summer.where(mask_domain == 1)
    if (model == "CNRM-CM5"):
        ds_avg = ds_summer
    else:
        ds_avg += ds_summer
# calculate ensemble average of gcms
ds_ens = ds_avg / 10.0
ds_ens = ds_ens - ds_ens_hist
# plot 

m = make_map(fs)
'''
vmax = ds_ens.max(['Latitude','Longitude'])
vmin = ds_ens.min(['Latitude','Longitude'])
'''
vmax = 50
vmin = -50

# trim off whitespace
ds_ens = ds_ens.sel(Latitude=slice(31,49.03), Longitude=slice(ds_ens.Longitude.min(), ds_ens.Longitude.max()))
x,y = m(ds_ens.Longitude, ds_ens.Latitude)
# img = ds_ens.plot(ax=ax, vmin=vmin, vmax=vmax, add_labels=False, cmap='bwr_r', add_colorbar=False)
img = m.pcolormesh(x, y, ds_ens.to_masked_array(), vmin=vmin, vmax=vmax, cmap='bwr_r') 

cbar = plt.colorbar(img)
cbar.set_ticks([np.linspace(vmin, vmax, 5, endpoint=True, dtype='int')])
cbar.set_label('Change \n in \n Soil \n Moisture \n Storage \n [mm]', rotation='horizontal', labelpad=lp)
ax.set_xlabel('Longitude', labelpad=20)
font = {'size' : fs}
plt.rc('font', **font)


## save plot
direc = '/raid/gergel/sm/plots/'
if not os.path.exists(direc):
    os.makedirs(direc) ## if directory doesn't exist, create it
plotname = 'sm_map' 
savepath = os.path.join(direc, plotname)
print ("saving figure to '%s'" % savepath)
plt.savefig(savepath, dpi=dpi)

