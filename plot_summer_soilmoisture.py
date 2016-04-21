
import matplotlib 
matplotlib.use('Agg')
import xarray as xray 
import os
import numpy as np
import sys
import pandas as pd
import matplotlib.pyplot as plt
from dfm_functions import make_map,make_mask, cmap_discretize 

fs = 40 ## fontsize
nbins = 11
lp = 10
dpi = 150

models = ['CNRM-CM5','NorESM1-M','IPSL-CM5A-MR','CanESM2','CCSM4','HadGEM2-CC365',
                   'HadGEM2-ES365','MIROC5','bcc-csm1-1-m','CSIRO-Mk3-6-0']

# models = ['CNRM-CM5'] 

scenarios = ['historical', 'rcp85']
chunks = ['1980s', '2050s']

direc = '/raid9/gergel/agg_snowpack/goodleap/'
filename = 'tmp_%s_TotalSoilMoist_%s.nc' % ("CNRM-CM5", "historical")
ds = xray.open_dataset(os.path.join(direc, filename))

# mask domain
mask_domain_mtns = make_mask('/raid9/gergel/agg_snowpack/gridcells_is_paper/mountains', ds.Latitude, ds.Longitude)
mask_domain_lowlands = make_mask('/raid9/gergel/agg_snowpack/gridcells_is_paper/lowlands', ds.Latitude, ds.Longitude)

f, axes = plt.subplots(nrows=2, ncols=2, figsize=(30, 30))

rows = [0, 1, 0, 1] 
cols = [0, 0, 1, 1] 

for i in np.arange(4):

	ax = axes[rows[i],cols[i]] 
	plt.sca(ax)

	# set font properties
        font = {'size' : fs}
        plt.rc('font', **font)

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
		ds_ens = ds_ens_fut - ds_ens_hist  
	
	# mask domain 
	if (i == 0) or (i == 2): 
		ds_ens = ds_ens.where(mask_domain_mtns == 1) 
	elif (i == 1) or (i == 3): 
		ds_ens = ds_ens.where(mask_domain_lowlands == 1) 

	# plot
 
	# trim off whitespace 
	ds_ens = ds_ens.sel(Latitude=slice(31,49.03), Longitude=slice(ds_ens.Longitude.min(), ds_ens.Longitude.max()))
	
	if i == 0:
		m = make_map(fs, label_parallels=True)
	elif i == 1: 
		m = make_map(fs, label_parallels=True, label_meridians=True) 
	elif i == 2: 
		m = make_map(fs) 
	else: 
		m = make_map(fs, label_meridians=True) 

	x,y = m(ds_ens.Longitude, ds_ens.Latitude)
	# discretize colormaps
	cmap_hist = cmap_discretize(plt.cm.viridis_r, 7)
	cmap_future = cmap_discretize(plt.cm.bwr_r, 8) 

	if i < 2: 
		vmin = -6
		vmax = 100
	else:
		vmin = -80
		vmax = 80

	if i < 2: 
		img_hist = m.pcolormesh(x, y, ds_ens.to_masked_array(), cmap=cmap_hist, vmin=vmin, vmax=vmax) 
	else: 
		img_future = m.pcolormesh(x, y, ds_ens.to_masked_array(), cmap=cmap_future, vmin=vmin, vmax=vmax)

	if i == 0: 
		ax.set_title('1970-1999 \n ')

	'''if i == 1: 
		ax.set_title('LOWLAND REGIONS \n ')''' 
	if i == 2: 
		ax.set_title('RCP 8.5 2050s \n ') 

# set font properties
font = {'size' : fs}
plt.rc('font', **font)


# get rid of whitespace between subplots
plt.subplots_adjust(wspace=0.1, hspace=None, left=0.05, right=0.98, top=0.9, bottom=0.2)

# create colorbar axes
cax1 = plt.axes([0.06, 0.1, 0.42, 0.05]) #[left,vertical, distance from left, height]
cax2 = plt.axes([0.55, 0.1, 0.42, 0.05]) 

vmax = 100
vmin = -6

cbar = plt.colorbar(img_hist, cax=cax1, orientation='horizontal', extend='both')
cbar.set_ticks([np.linspace(vmin, vmax, 8, endpoint=True, dtype='int')])
cbar.set_label('Soil Moisture Storage [mm]', rotation='horizontal', labelpad=lp)

vmax = 80
vmin = -80

cbar = plt.colorbar(img_future, cax=cax2, orientation='horizontal', extend='both')
cbar.set_ticks([np.linspace(vmin, vmax, 9, endpoint=True, dtype='int')])
cbar.set_label('Change in Soil Moisture Storage [mm]', rotation='horizontal', labelpad=lp)

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

